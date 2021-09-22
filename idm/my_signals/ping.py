from idm.objects import dp, MySignalEvent, LongpollEvent
from datetime import datetime

pings = {
    "выстрел": "прострел",
    "ток": "🔌",
    "пиу": "ПАУ",
    "тик": "ТОК",
    "ping": "PONG",
    "king": "The Lion King*",
    "tick": "tick-tock-tack"
}


@dp.my_signal_event_register(*pings.keys())
def ping(event: MySignalEvent) -> str:
    c_time = datetime.now().timestamp()
    delta = round(c_time - event.msg['date'], 2)

    event.msg_op(2, event.responses['ping_myself'].format(
            время=delta,
            ответ=pings.get(event.command),
            обработано=round(datetime.now().timestamp() - event.time - event.vk_response_time, 2),  # noqa
            пингвк=round(event.vk_response_time, 2)
        ))
    return "ok"


@dp.my_signal_event_register('пингб', skip_receiving=True)
def ping_bf(event: MySignalEvent) -> str:
    event.msg_op(1, 'PONG')
    return "ok"


@dp.longpoll_event_register(*pings.keys())
def ping_lp(event: LongpollEvent) -> str:
    c_time = datetime.now().timestamp()
    delta = round(c_time - event.msg['date'], 2)
    event.msg_op(2, f'{pings.get(event.command)} LP\nОтвет через {delta}сек.')
    return "ok"
