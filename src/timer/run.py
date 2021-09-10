# coding:utf-8

import os
import sys
reload(sys)
sys.setdefaultencoding('utf8')

project_src_dir = os.path.dirname(os.path.realpath(__file__))
project_src_dir = os.path.dirname(project_src_dir)
sys.path.insert(0, project_src_dir)

from apscheduler.schedulers.gevent import BlockingScheduler

from timer.RestTimer import ActivitiesTimer
from timer.RestTimer import UserData
from timer.RestTimer import IdentitiesData
from timer.RestTimer import StatisticsData
from timer.RestTimer import EveryFewMinutesExe

if __name__ == "__main__":
    every_few_minutes_exe = EveryFewMinutesExe()
    activity_timer = ActivitiesTimer()
    user_data = UserData()
    identities_data = IdentitiesData()
    statistics_data = StatisticsData()

    sched = BlockingScheduler()
    # 改变活动状态
    sched.add_job(activity_timer.change_activity_status, 'interval', seconds=3)
    # 已分配的优惠券状态修改
    sched.add_job(activity_timer.change_coupe_status, 'interval', seconds=20)
    # 更新活动相关的数据
    sched.add_job(activity_timer.update_coupon_data, 'interval', seconds=60)
    # 邀请返券
    sched.add_job(
        activity_timer.invited_users_give_coupon, 'interval', seconds=60)
    # 用户乘车次数汇总
    sched.add_job(user_data.user_take_bus_count, 'interval', seconds=60)
    # 用户身份状态改变
    sched.add_job(
        identities_data.change_user_identity_status, 'interval', seconds=20)
    sched.add_job(statistics_data.statistics_yesterday_data,
                  'interval', seconds=10)
    sched.add_job(statistics_data.statistics_passenger_flow,
                  'interval', seconds=60 * 60)

    # 每五分钟执行
    sched.add_job(func=every_few_minutes_exe.every_few_minutes_execute,
                  trigger='cron', day="*", hour="*", minute="*/5")

    sched.start()
