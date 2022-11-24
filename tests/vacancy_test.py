import unittest

from datetime import datetime, timedelta, timezone

from src.vasya.vacancy import Vacancy, Salary, currency_dict, experience_dict


class TestVacancy(unittest.TestCase):
    def test_init(self):
        vacancy = Vacancy(
            name="test",
            salary_from="10000",
            salary_to="20000",
            salary_currency="RUR",
            area_name="Москва",
            published_at="1970-01-01T12:00:00+0300",
            description="<p>test test</p>",
            key_skills="test\ntest",
            experience_id="between3And6",
            premium="FALSE",
            employer_name="test",
            salary_gross="TRUE",
        )
        self._test_small_init(vacancy)
        self._test_full_init(vacancy)
        self._test_formatted_data(vacancy)

    def _test_small_init(self, vacancy: Vacancy):
        self.assertEqual(vacancy.name, "test")
        self.assertEqual(vacancy.salary_rub, (10000 + 20000) / 2)
        self.assertEqual(vacancy.area_name, "Москва")
        self.assertEqual(
            vacancy.published_at,
            datetime(1970, 1, 1, 12, 0, 0, 0, timezone(timedelta(hours=3))),
        )

    def _test_full_init(self, vacancy: Vacancy):
        self.assertEqual(vacancy.description, "test test")
        self.assertEqual(vacancy.key_skills, ["test", "test"])
        self.assertEqual(vacancy.experience, experience_dict["between3And6"])
        self.assertEqual(vacancy.premium, "Нет")
        self.assertEqual(vacancy.employer_name, "test")
        self.assertEqual(vacancy.salary, Salary(10000, 20000, True, "RUR"))
        self.assertEqual(vacancy.salary_rub, float(vacancy.salary))

    def _test_formatted_data(self, vacancy: Vacancy):
        data = list(vacancy.formatted_data())
        self.assertEqual(data[0], "test")
        self.assertEqual(data[1], "test test")
        self.assertEqual(data[2], "test\ntest")
        self.assertEqual(data[3], str(experience_dict["between3And6"]))
        self.assertEqual(data[4], "Нет")
        self.assertEqual(data[5], "test")
        self.assertEqual(data[6], str(vacancy.salary))
        self.assertEqual(data[7], "Москва")
        self.assertEqual(
            data[8],
            datetime(1970, 1, 1, 12, 0, 0, 0, timezone(timedelta(hours=3))).strftime(
                "%d.%m.%Y"
            ),
        )

    def test_salary(self):
        currency = currency_dict["USD"]
        salary = Salary(400, 500, True, currency)
        self.assertEqual(salary.salary_from, 400)
        self.assertEqual(salary.salary_to, 500)
        self.assertEqual(salary.salary_currency, "USD")
        self.assertEqual(salary.salary_gross, True)

        salary_rub = salary.to_rub()
        self.assertEqual(salary_rub.salary_from, 400 * currency)
        self.assertEqual(salary_rub.salary_to, 500 * currency)
        self.assertEqual(salary_rub.salary_currency, "RUR")
        self.assertEqual(salary_rub.salary_gross, True)

        comp_salary = Salary(300, 500, True, currency)
        self.assertEqual(comp_salary < salary, True)
        self.assertEqual(comp_salary < salary_rub, True)
