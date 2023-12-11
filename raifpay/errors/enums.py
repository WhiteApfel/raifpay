from enum import StrEnum


class ERROR(StrEnum):
    ACCOUNT_IS_NOT_REGISTERED = (
        "Указан неверный счет. Проверьте его или удалите. Параметр является"
        " необязательным"
    )
    INVALID_REQUEST = "Не передан обязательный параметр"
    QR_EXPIRATION_DATE_NOT_VALID = "Неверная дата истечения QR-кода"
    MERCHANT_NOT_REGISTERED = "Партнер с ID * не зарегистрирован"
    ORDER_NUMBER_ALREADY_REGISTERED = (
        "QR-код с номером заказа *, партнера * и успешными платежами уже"
        " зарегистрирован"
    )
    INVALID_PAYMENT_AMOUNT = "Передана некорректная сумма платежа"
    SBP_MERCHANT_ID_IS_MISSING = "SbpMerchantId партнера не указан"
    DYNAMIC_QR_WITHOUT_AMOUNT = "Не передана сумма для динамического QR-кода"
    INVALID_ORDER = "В номере заказа поддерживаются A-z09_-."
    NOT_FOUND = "QR-код не найден у данного партнера"
    REFUND_INSUFFICIENT_FUNDS = "Сумма возврата больше суммы остатка по платежу"
    INVALID_REFUND_AMOUNT = "Сумма возврата не может быть меньше 1 копейки"
    REFUND_NOT_FOUND = "Возврат с refundId * не найден"
    WRONG_QR_STATUS = "Нельзя сменить статус QR-кода с * на *"

    def __getitem__(self, item: str):
        item = item.removeprefix("ERROR.")
        return super().__getitem__(item)
