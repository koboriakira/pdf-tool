from dataclasses import dataclass
from datetime import date, time

import yaml

from pdf_writer import InsertProperty


@dataclass
class Reserver:
    name: str  # 利用者名
    insurance_number: int | None = None  # 保険証の記号


@dataclass
class Reservation:
    reservation_date: str  # 予約日
    reservation_time: str  # 予約時間
    member_count: int  # 参加者数
    course_name: str  # コース名
    insurance_symbol_number: int  # 保険証の記号
    business_operator_name: str  # 事業者名
    representative_name: str  # 利用代表者名
    work_phone_number: str  # 勤務先電話番号
    reservers: list[Reserver] | None = None  # 利用者リスト

    @staticmethod
    def from_config_yaml() -> "Reservation":
        with open("src/itskenpo/config.yaml", "r") as yml:
            config = yaml.safe_load(yml)
            reservers = []
            for reserver in config["reservers"]:
                reservers.append(Reserver(**reserver))
            return Reservation(reservers=reservers, **config["reservation"])

    def to_insert_properties(self) -> list[InsertProperty]:
        insert_properties = []
        reservation_date_ = date.fromisoformat(self.reservation_date)
        reservation_time_ = time.fromisoformat(str(self.reservation_time))
        insert_properties.append(
            InsertProperty(
                pos=(135, 182), text=str(reservation_date_.month), label="利用月"
            )
        )
        insert_properties.append(
            InsertProperty(
                pos=(180, 182), text=str(reservation_date_.day), label="利用日"
            )
        )
        insert_properties.append(
            InsertProperty(
                pos=(135, 210),
                text=str(reservation_time_.hour),
                label="利用時間(時)",
            )
        )
        insert_properties.append(
            InsertProperty(
                pos=(178, 210),
                text=str(reservation_time_.strftime("%M")),
                label="利用時間(分)",
            )
        )
        insert_properties.append(
            InsertProperty(
                pos=(200, 238), text=str(self.member_count), label="内部メンバー人数"
            )
        )
        insert_properties.append(
            InsertProperty(pos=(155, 290), text=self.course_name, label="コース名")
        )
        insert_properties.append(
            InsertProperty(
                pos=(420, 184),
                text=str(self.insurance_symbol_number),
                label="保険証の記号",
            )
        )
        insert_properties.append(
            InsertProperty(
                pos=(380, 211),
                text=self.business_operator_name,
                label="事業者名",
            )
        )
        insert_properties.append(
            InsertProperty(
                pos=(410, 247),
                text=self.representative_name,
                label="利用代表者名",
            )
        )
        insert_properties.append(
            InsertProperty(
                pos=(396, 290),
                text=self.work_phone_number,
                label="勤務先電話番号",
            )
        )
        if self.reservers is None:
            return insert_properties

        for i, reserver in enumerate(self.reservers):
            insert_properties.append(
                InsertProperty(
                    pos=(80, 375 + i * 23),
                    text=str(reserver.insurance_number)
                    if reserver.insurance_number
                    else "",
                    label=f"利用者{i+1}の保険証の記号",
                )
            )
            insert_properties.append(
                InsertProperty(
                    pos=(180, 375 + i * 23),
                    text=reserver.name,
                    label=f"利用者{i+1}の利用者名",
                )
            )
        return insert_properties


if __name__ == "__main__":
    # python -m src.itskenpo.reservation
    reservation = Reservation.from_config_yaml()
    print(reservation)
    print(reservation.to_insert_properties())
