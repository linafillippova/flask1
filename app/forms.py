from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, ValidationError
import re

class PhoneForm(FlaskForm):
    phone_number = StringField('Номер телефона', validators=[DataRequired()])
    submit = SubmitField('Проверить')

    def validate_phone_number(self, phone_number):
        phone_number_str = phone_number.data  # Извлекаем значение из поля

        # Добавлена проверка на недопустимые символы
        if not re.match(r'^[\d\s()+\-.]+$', phone_number_str):
            raise ValidationError("Недопустимый ввод. В номере телефона встречаются недопустимые символы.")

        cleaned_number = re.sub(r'[^\d]', '', phone_number_str) # Удаляем все кроме цифр

        if len(cleaned_number) < 10 or len(cleaned_number) > 11:
            raise ValidationError("Недопустимый ввод. Неверное количество цифр.")

        # Форматирование номера
        if len(cleaned_number) == 11 and cleaned_number.startswith('7'):
            cleaned_number = "8" + cleaned_number[1:]  # Заменяем "7" на "8"
        elif len(cleaned_number) == 10:
            cleaned_number = "8" + cleaned_number # Добавляем "8" в начале

        formatted_number = f"{cleaned_number[:1]}-{cleaned_number[1:4]}-{cleaned_number[4:7]}-{cleaned_number[7:9]}-{cleaned_number[9:]}"

        return formatted_number