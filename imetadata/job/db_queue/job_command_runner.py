# -*- coding: utf-8 -*- 
# @Time : 2020/8/12 17:28 
# @Author : 王西亚
# @File : job_command_runner.py

from __future__ import absolute_import

import time
from multiprocessing import Queue, Lock, Manager

from imetadata.base.c_logger import CLogger
from imetadata.base.c_result import CResult
from imetadata.database.c_factory import CFactory
from imetadata.schedule.job.c_dbQueueJob import CDBQueueJob
from imetadata.service.c_controlCenter import CControlCenter


class job_command_runner(CDBQueueJob):
    __cmd_queue__ = None
    __locker__ = None
    __shared_control_center_info__ = None
    __control_center_obj__: CControlCenter = None

    def before_execute(self):
        self.__cmd_queue__ = Queue()
        self.__locker__ = Lock()
        self.__shared_control_center_info__ = Manager().dict()
        self.__control_center_obj__ = CControlCenter(self.__cmd_queue__, self.__locker__,
                                                     self.__shared_control_center_info__)
        self.__control_center_obj__.start()
        CLogger().debug('控制中心进程{0}已经启动！'.format(self.__control_center_obj__.pid))
        time.sleep(5)

    def get_mission_seize_sql(self) -> str:
        return '''
update sch_center_mission 
set scmprocessid = '{0}', scmstatus = 2
where scmid = (
  select scmid  
  from   sch_center_mission 
  where  scmstatus = 1 
  limit 1
  for update skip locked
)
        '''.format(self.SYSTEM_NAME_MISSION_ID)

    def get_mission_info_sql(self):
        return '''
select scmid, scmtitle, scmCommand, scmTrigger, scmAlgorithm, scmParams::text 
from sch_center_mission 
where scmprocessid = '{0}'        
        '''.format(self.SYSTEM_NAME_MISSION_ID)

    def get_abnormal_mission_restart_sql(self) -> str:
        return '''
update sch_center_mission 
set scmstatus = 1, scmprocessid = null 
where scmstatus = 2 
        '''

    def process_mission(self, dataset, is_retry_mission: bool):
        mission_id = dataset.value_by_name(0, 'scmid', '')
        mission_title = dataset.value_by_name(0, 'scmtitle', '')

        CLogger().info('系统正在处理任务{0}.{1}'.format(mission_id, mission_title))

        command_content = dataset.value_by_name(0, 'scmcommand', '')
        CLogger().info('任务命令：{0}'.format(command_content))

        if mission_id == '':
            return CResult.merge_result(CResult.Failure, '任务标示为空，无法处理!')

        if command_content != '':
            command_queue_item: dict = {self.NAME_CMD_ID: mission_id}
            command_queue_item[self.NAME_CMD_TITLE] = mission_title
            command_queue_item[self.NAME_CMD_COMMAND] = command_content
            command_queue_item[self.NAME_CMD_ALGORITHM] = dataset.value_by_name(0, 'scmalgorithm', '')
            command_queue_item[self.NAME_CMD_TRIGGER] = dataset.value_by_name(0, 'scmtrigger', '')
            command_queue_item[self.NAME_CMD_PARAMS] = dataset.value_by_name(0, 'scmparams', '')

            CLogger().info('系统正在处理任务{0}.{1}, 开始发送任务队列'.format(mission_id, mission_title))
            self.__cmd_queue__.put(command_queue_item)

        CFactory().give_me_db().execute(
            '''
            update sch_center_mission 
            set scmstatus = 0
            where scmid = '{0}'
            '''.format(mission_id)
        )
        return CResult.merge_result(CResult.Success, '新的并行处理器已经创建完毕!')

    def before_stop(self):
        # 给控制中心发送退出信息，等待控制中心退出
        if self.__control_center_obj__ is not None:
            self.__cmd_queue__.put(None)
            self.__control_center_obj__.join()
            CLogger().debug('控制中心进程已经关闭！')
