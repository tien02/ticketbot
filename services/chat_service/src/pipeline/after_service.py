import datetime
import re

import psycopg2
from config import data_settings
from schema import UserMessage

from ._base import BasePipeline


class AfterServicesPipeline(BasePipeline):
    CLASSIFY_AFTER_SERVICES_PROMPT = """
    Classify the following message into one of these categories:
    - Cancel booking
    - Change time

    Message: "{user_message}"
    Respond with only one of the categories.
    """

    EXTRACT_DATE_PROMPT = """
    The user wants to change the time of their ticket.

    User message: "{user_msg}"

    This is their booking information:
    {ticket_info}

    Task: From the message, extract the new trip date (format: YYYY-MM-DD).
    Respond with datetime only.
    """

    conn = psycopg2.connect(
        dbname=data_settings.POSTGRES_DB,
        user=data_settings.POSTGRES_USER,
        password=data_settings.POSTGRES_PASSWORD,
        host=data_settings.POSTGRES_HOST,
        port=data_settings.POSTGRES_PORT,
    )

    def run(self, usr_msg: UserMessage) -> str:
        category = self._classify_service(msg=usr_msg).lower()

        pattern_handlers = [
            (re.compile(r"cancel|hủy", re.IGNORECASE), self._cancel_booking),
            (
                re.compile(r"change.*time|thay đổi.*giờ", re.IGNORECASE),
                self._change_time,
            ),
        ]
        for pattern, handler in pattern_handlers:
            if pattern.search(category):
                return handler(usr_msg=usr_msg)

        return (
            "Xin lỗi, tôi không hiểu yêu cầu của bạn. "
            "Vui lòng liên hệ với bộ phận hỗ trợ khách hàng để được giúp đỡ."
        )

    def _classify_service(self, msg: str) -> str:
        prompt = self.CLASSIFY_AFTER_SERVICES_PROMPT.format(user_message=msg)
        return self.get_text_response(prompt)

    def _cancel_booking(self, usr_msg: UserMessage) -> str:
        user_id = usr_msg.user_id

        with self.conn.cursor() as cur:
            cur.execute(
                "DELETE FROM booking_tickets WHERE user_id = %s RETURNING booking_id;",
                (user_id,),
            )
            deleted = cur.fetchone()
            self.conn.commit()

        if deleted:
            return f"{user_id}, vé của bạn (ID: {deleted[0]}) đã được hủy thành công."
        return f"{user_id}, hiện tại bạn không có vé nào để hủy."

    def _change_time(self, usr_msg: UserMessage) -> str:
        user_id = usr_msg.user_id
        msg = usr_msg.message

        with self.conn.cursor() as cur:
            cur.execute(
                "SELECT booking_id, start_location, destination, trip_date, seats "
                "FROM booking_tickets WHERE user_id = %s ORDER BY trip_date;",
                (user_id,),
            )
            tickets = cur.fetchall()

        if not tickets:
            return f"{user_id}, hiện tại bạn không có vé nào để đổi thời gian."

        ticket_info = "\n".join(
            f"- Booking ID: {t[0]}, {t[1]} → {t[2]}, Ngày: {t[3]}" for t in tickets
        )

        result = self._parse_date(msg=msg, ticket_info=ticket_info)
        if not result:
            return f"{user_id}, bạn muốn đổi vé sang ngày nào?"

        try:
            new_date = datetime.date.fromisoformat(result)
        except ValueError:
            return f"{user_id}, ngày {result} không hợp lệ. Vui lòng nhập lại theo định dạng YYYY-MM-DD."

        with self.conn.cursor() as cur:
            cur.execute(
                "UPDATE booking_tickets SET trip_date = %s WHERE user_id = %s RETURNING booking_id;",
                (new_date, user_id),
            )
            updated = cur.fetchone()
            self.conn.commit()

        if updated:
            return f"{user_id}, vé của bạn (ID: {updated[0]}) đã được đổi sang ngày {new_date}."
        return f"{user_id}, không tìm thấy vé để đổi thời gian."

    def _parse_date(self, msg: str, ticket_info: str) -> str | None:
        prompt = self.EXTRACT_DATE_PROMPT.format(user_msg=msg, ticket_info=ticket_info)
        response = self.get_text_response(prompt).strip()
        match = re.search(r"\b(\d{4}-\d{2}-\d{2})\b", response)
        return match.group(1) if match else None
