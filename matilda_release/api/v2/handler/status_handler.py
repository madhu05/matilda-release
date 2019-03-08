from matilda_release.util import encoder
import matilda_release.util.status_engine as stts_engine


enc = encoder.AESCipher()

def update_task_stats(task_id, data):
    return stts_engine.check_and_update_task(task_id=task_id, data=data)
    # task_data = db_api.get_task(task_id=task_id)
    # data['output'] = enc.encrypt(str(data.get('output')))
    # data['status'] = data.get('status')
    # if data['status'].lower() == 'in progress':
    #     data['actual_start_dt'] = datetime.now()
    # elif data['status'].lower() in ['success', 'failed']:
    #     data['actual_end_dt'] = datetime.now()
    # resp = db_api.update_task(task_id, data)
    # stage_handler.check_and_update_stage()
    # return resp

