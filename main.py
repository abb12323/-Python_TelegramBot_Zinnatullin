import os
import datetime
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
from custom_calendar import Calendar
from db import conn

calendar = Calendar(conn)


def main():
    API_TOKEN = '7647019759:AAFPwYG-6QEikVKQH1BLNvUf_ig7l85zbko'

    # Инициализация объекта Updater
    updater = Updater(token=API_TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    def event_create_handler(update: Update, context: CallbackContext):
        parts = update.message.text.split()
        if len(parts) < 5:
            update.message.reply_text(
                "Неверный формат команды. Используйте: /create_event Название Дата Время Детали")
            return
        event_name, event_date, event_time, *event_details = parts
        event_details = " ".join(event_details)
        event_id = calendar.create_event(
            event_name, event_date, event_time, event_details)
        update.message.reply_text(
            f"Событие \"{event_name}\" создано с номером {event_id}.")

    def event_read_handler(update: Update, context: CallbackContext):
        parts = update.message.text.split()
        if len(parts) != 2:
            update.message.reply_text(
                "Неверный формат команды. Используйте: /read_event НомерСобытия")
            return
        event_id = parts
        event = calendar.read_event(event_id)
        if event:
            reply = f"{event['name']} ({event['date']} {event['time']})\nДетали: {event['details']}"
            update.message.reply_text(reply)
        else:
            update.message.reply_text("Событие с данным номером не найдено.")

    def event_edit_handler(update: Update, context: CallbackContext):
        parts = update.message.text.split()
        if len(parts) < 5:
            update.message.reply_text(
                "Неверный формат команды. Используйте: /edit_event Номер Название Дата Время Детали")
            return
        event_id, event_name, event_date, event_time, *event_details = parts
        event_details = " ".join(event_details)
        event_to_edit = {"name": event_name, "date": event_date,
                         "time": event_time, "details": event_details}
        success = calendar.edit_event(event_id, event_to_edit)
        if success:
            update.message.reply_text(
                f"Событие №{event_id} успешно обновлено.")
        else:
            update.message.reply_text("Событие с данным номером не найдено.")

    def event_delete_handler(update: Update, context: CallbackContext):
        parts = update.message.text.split()
        if len(parts) != 2:
            update.message.reply_text(
                "Неверный формат команды. Используйте: /delete_event НомерСобытия")
            return
        event_id = parts
        success = calendar.delete_event(event_id)
        if success:
            update.message.reply_text(f"Событие №{event_id} успешно удалено.")
        else:
            update.message.reply_text("Событие с данным номером не найдено.")

    def events_list_handler(update: Update, context: CallbackContext):
        all_events = calendar.list_events()
        if not all_events:
            update.message.reply_text("Нет запланированных событий.")
        else:
            result = []
            for event in all_events:
                result.append(
                    f"{event['name']} ({event['date']} {event['time']}) - #{event['id']}: {event['details']}")
            update.message.reply_text("\n".join(result))

    # Регистрация обработчиков команд
    dispatcher.add_handler(CommandHandler(
        'create_event', event_create_handler))
    dispatcher.add_handler(CommandHandler('read_event', event_read_handler))
    dispatcher.add_handler(CommandHandler('edit_event', event_edit_handler))
    dispatcher.add_handler(CommandHandler(
        'delete_event', event_delete_handler))
    dispatcher.add_handler(CommandHandler('events_list', events_list_handler))

    # Запуск бота
    updater.start_polling()
    print("Бот запущен и ждёт ваших команд...")
    updater.idle()


if __name__ == '__main__':
    main()
