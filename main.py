import asyncio
from aiohttp import ClientSession, ClientTimeout
from rubpy import Client, handlers, models, Message
import sqlite3
import json

DATABASE = 'g0DW6Jm084d23b926d7bbfd23247ebc3'


async def main():
    async with ClientSession(timeout=ClientTimeout(5)) as CS:
        async with Client(session='MyBot') as client:
            @client.on(handlers.MessageUpdates(models.is_private))
            async def on_message(update: Message):
                author_guid = update.author_guid
                object_guid = update.object_guid
                message_id = update.message_id
                print(object_guid, '----------', author_guid)
                t = update.raw_text
                user = await client.get_user_info(author_guid)
                print(t)
                a = await client.forward_messages(from_object_guid=object_guid, to_object_guid=DATABASE,
                                                  message_ids=[message_id])
                print(a['message_updates'][0]['message']['type'])
                result = a['message_updates'][0]['message']['type']
                if 'DL-' in t:
                    result = result + 'qq'
                if result != 'Text':
                    if 'UP-' in t and len(t[t.index('-') + 1:]) <= 8:
                        ddl = 'DL-' + t[t.index('-') + 1:]
                        print(a['message_updates'])
                        b = a['message_updates']
                        d = {}

                        for update in b:
                            c = update['message_id']
                            key = t[t.index('-') + 1:]

                            if key in d:
                                print(f"Duplicate key: {key}. Ignoring...")
                            else:
                                d[key] = c

                        # ذخیره دیکشنری در پایگاه داده SQLite
                        conn = sqlite3.connect('database.db')
                        cursor = conn.cursor()
                        cursor.execute('CREATE TABLE IF NOT EXISTS my_table (key TEXT PRIMARY KEY, value INTEGER)')
                        for key, value in d.items():
                            try:
                                cursor.execute('INSERT INTO my_table (key, value) VALUES (?, ?)', (key, value))
                                await client.send_message(object_guid=object_guid, reply_to_message_id=message_id,
                                                          message='پیام شما دریافت شد.'
                                                                  'برای دریافت آن از تگ : \n \n'
                                                                  f'{ddl}\n \n'
                                                                  f'استفاده کنید.')
                            except sqlite3.IntegrityError:
                                print(f"Duplicate key: {key}. Ignoring...")
                                await client.send_message(object_guid=object_guid, reply_to_message_id=message_id,
                                                          message='کلید استفاده شده تکراریست.')
                        conn.commit()

                        # چاپ داده‌های موجود در دیتابیس
                        cursor.execute('SELECT * FROM my_table')
                        rows = cursor.fetchall()
                        for row in rows:
                            print(row)

                        conn.close()



                    elif 'DL-' in t:

                        # انجام عملیات مربوط به 'DL-'

                        # مثلاً اجرای یک کوئری SELECT برای بازیابی داده‌های مورد نیاز

                        # و نمایش آن‌ها

                        conn = sqlite3.connect('database.db')

                        cursor = conn.cursor()

                        cursor.execute('SELECT * FROM my_table')

                        rows = cursor.fetchall()

                        for row in rows:
                            print(row)

                        conn.close()

                        cc = t[t.index('-') + 1:]

                        conn = sqlite3.connect('database.db')

                        cursor = conn.cursor()

                        cursor.execute("SELECT value FROM my_table WHERE key = ?", (cc,))

                        result = cursor.fetchone()

                        conn.close()

                        if result is not None:

                            databasekey = cc

                            databasevalue = result[0]

                            print(f"Found key: {databasekey}, Value: {databasevalue}")
                            await client.forward_messages(from_object_guid=DATABASE, to_object_guid=object_guid,
                                                          message_ids=[databasevalue])

                        else:

                            print("Key not found in the database.")
                            await client.send_message(object_guid=object_guid, reply_to_message_id=message_id,
                                                      message='یافت نشد.')
                    elif len(t) >= 8:
                        await client.send_message(object_guid=object_guid, reply_to_message_id=message_id,
                                                  message='طول تگ شما بیشتر از 8 کاراکتر است.')
                else:
                    await client.send_message(object_guid=object_guid, reply_to_message_id=message_id,
                                              message='نوع پیام ارسالی نباید متنی باشد')

            await client.run_until_disconnected()


if __name__ == '__main__':
    asyncio.run(main())
