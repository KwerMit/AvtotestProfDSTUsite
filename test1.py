from selenium import webdriver
import time
import unittest
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By

class ProfDSTU(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome('C:/Users/Mit-PC/PycharmProjects/firstpr/venv/chromedriver.exe')
        self.driver.get('https://site.dev.profdstu.ru')
        login = self.driver.find_element_by_xpath('//input[1]')
        login.send_keys("kwermit")
        psw = self.driver.find_element_by_id('input-15')
        psw.send_keys("cvhd5b16")
        login.send_keys(Keys.ENTER)
        time.sleep(2)

    def tearDown(self):
        self.driver.quit()

    # def test_01(self): #Авторизация с верными данными
    #     driver = self.driver
    #     driver.implicitly_wait(10)
    #     assert "Павлов А.А." in driver.find_element_by_class_name("mt-10.mb-10").text
    #     assert "Контингент" in driver.find_element_by_class_name("v-card__title").text
    #     driver.find_element_by_class_name("v-responsive__content").click()
    #     driver.find_element_by_xpath("//body/div/div/div/div/div[1]").click()
    #
    # def test_02(self): #Сообщение при авторизации с неверными данными
    #     driver = self.driver
    #     driver.implicitly_wait(10)
    #     driver.find_element_by_class_name("v-responsive__content").click()
    #     driver.find_element_by_xpath("//body/div/div/div/div/div[1]").click()
    #     time.sleep(2)
    #
    #     login = driver.find_element_by_xpath('//input[1]')
    #     login.send_keys("kwermit")
    #     psw = driver.find_element_by_id('input-94')
    #     psw.send_keys("cvhd5b15")
    #     login.send_keys(Keys.ENTER)
    #     time.sleep(2)
    #     msg1 = driver.find_element_by_class_name("v-alert__content").text
    #
    #     login.send_keys(Keys.BACKSPACE)
    #     login.send_keys("r") #Неправильны логин
    #     psw.send_keys(Keys.BACKSPACE)
    #     psw.send_keys("6") #Правильный пароль
    #     psw.send_keys(Keys.ENTER)
    #     msg2 = driver.find_element_by_class_name("v-alert__content").text
    #     assert msg1==msg2
    #
    # def test_03(self): #Поиск по номеру зачетной книжки
    #     driver = self.driver
    #     driver.implicitly_wait(10)
    #
    #     driver.find_elements_by_xpath("//tr[1]/td[1]/div[1]") #Проверка, что страница загрузилась полностью
    #     search = driver.find_element_by_id("input-62")
    #     search.send_keys("1676431") #Номер зачетной книжки
    #     search.send_keys(Keys.ENTER)
    #     time.sleep(1)
    #     FIO = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//td[@class='text-left']/div[1]")))
    #     assert "Павлов Артем Александрович" == FIO.text
    #     assert "1676431" == driver.find_element_by_xpath('//td[9]/div[1]').text

    def test_04(self): #Поиск по ФИО студента
        driver = self.driver
        driver.implicitly_wait(10)
        driver.find_elements_by_xpath("//tr[1]/td[1]/div[1]")

        search = driver.find_element_by_id("input-62")
        search.send_keys("Павлов Артем Александрович")  # ФИО Студента
        search.send_keys(Keys.ENTER)
        time.sleep(4)
        FIO = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//td[@class='text-left']/div[1]")))
        assert "Павлов Артем Александрович" in FIO.text
        assert "1676431" == driver.find_element_by_xpath('//td[9]/div[1]').text

    def test_05(self): #Фильтрация по факультету
        driver = self.driver
        driver.implicitly_wait(10)
        driver.find_element_by_xpath("//tr[1]/td[1]/div[1]")

        driver.find_element_by_xpath("//div[@class='row']/div[3]/button[1]").click()
        time.sleep(1)
        assert "Факультет" in driver.find_element_by_xpath("//div[@class='v-select__slot']/label[1]").text
        pole = driver.find_element_by_id("input-135")
        pole.send_keys("ИиВТ")
        pole.send_keys(Keys.ENTER)
        assert "ИиВТ" == pole.get_attribute("value")
        search = driver.find_element_by_xpath("//nav/div/div/div/div/div[9]") #Кнопка "Поиск"
        search.click()
        time.sleep(5)
        tfaculty = driver.find_elements_by_xpath("//tr/td[4]/div[1]")
        for i in tfaculty: #Проверка, что в каждой строке в поле факультета есть нужное значение
            assert "ИиВТ" in i.text


    def test_06(self):  # Фильтрация по группе
        driver = self.driver
        driver.implicitly_wait(10)
        driver.find_element_by_xpath("//tr[1]/td[1]/div[1]")
        driver.find_element_by_xpath("//button[span[contains(text(), 'Фильтр')]]").click()

        faculty = driver.find_element_by_xpath("//div[label[contains(text(), 'Факультет')]]/input")
        faculty.send_keys("ИиВТ")
        faculty.send_keys(Keys.ENTER)
        time.sleep(0.5)
        group = driver.find_element_by_xpath("//div[label[contains(text(), 'Группа')]]/input")
        group.click()
        group.send_keys("ВПМ11")
        group.send_keys(Keys.ENTER)
        search = driver.find_element_by_xpath("//div[button[span[contains(text(),'Поиск')]]]")  # Кнопка "Поиск"
        search.click()
        time.sleep(4)
        tgrpoup = driver.find_elements_by_xpath("//tr/td[5]/button")
        for i in tgrpoup:  # Проверка, что в каждой строке стобца группы нужное значение
            assert "ВПМ11" in i.text

    def test_07(self):  # Фильтрации по признаку наличия стипендии
        driver = self.driver
        driver.implicitly_wait(10)
        driver.find_element_by_xpath("//tr[1]/td[1]/div[1]")
        driver.find_element_by_xpath("//div[@class='row']/div[3]/button[1]").click()

        driver.find_element_by_xpath("//div/div[3]/div/div/div/div").click()# Поле стипендии
        driver.find_element_by_xpath("//body/div/div[3]/div/div").click()# Выбор её наличия
        driver.find_element_by_xpath("//div[button[span[contains(text(),'Поиск')]]]").click() # Кнопка "Поиск"
        time.sleep(5)
        tgrant = driver.find_elements_by_xpath("//tr/td[3]/div/i")
        for i in tgrant:  # Проверка, что в каждой строке стобца группы нужное значение
            assert "plus" in i.get_attribute("class")

    # def test_08(self):  # Фильтрации по признаку отсутствия стипендии. Баг
    #     driver = self.driver
    #     driver.implicitly_wait(10)
    #     driver.find_element_by_xpath("//tr[1]/td[1]/div[1]")
    #     driver.find_element_by_xpath("//div[@class='row']/div[3]/button[1]").click()
    #
    #     driver.find_element_by_xpath("//div/div[3]/div/div/div/div").click()  # Поле стипендии
    #     driver.find_element_by_xpath("//body/div/div[3]/div/div[2]").click()  # Выбор её наличия
    #     driver.find_element_by_xpath("//div[button[span[contains(text(),'Поиск')]]]").click()  # Кнопка "Поиск"
    #     time.sleep(5)
    #     tgrant = driver.find_elements_by_xpath("//tr/td[3]/div[1]/i")
    #     for i in tgrant:  # Проверка, что в каждой строке стобца группы нужное значение
    #         assert "minus" in i.get_attribute("class")

    def test_09(self):  # Фильтрация по курсам
        driver = self.driver
        driver.implicitly_wait(10)
        driver.find_element_by_xpath("//tr[1]/td[1]/div[1]") #Проверка загрузки таблицы
        driver.find_element_by_xpath("//div[@class='row']/div[3]/button[1]").click() #Открытие фильтра

        course = driver.find_element_by_xpath("//div[label[contains(text(), 'Курс')]]") #Поле курса
        course.click()
        assert "active" in driver.find_element_by_xpath("//div[div[div[div[div[contains(text(), '1 курс')]]]]]").get_attribute("class")
        course1 = driver.find_element_by_xpath("//div[div[div[contains(text(), '1 курс')]]]")
        course1.click()
        assert "true" in course1.get_attribute("aria-selected")#Чекбокс активен
        search = driver.find_element_by_xpath("//div[button[span[contains(text(),'Поиск')]]]")  # Кнопка "Поиск"
        search.click()
        time.sleep(3)
        for i in driver.find_elements_by_xpath("//tr/td[8]/div[1]"):
            assert '1' in i.text

        course.click()
        course4 = driver.find_element_by_xpath("//div[div[div[contains(text(), '4 курс')]]]")
        course4.click()
        assert "true" in course1.get_attribute("aria-selected")
        assert "true" in course4.get_attribute("aria-selected")
        course3 = driver.find_element_by_xpath("//div[div[div[contains(text(), '3 курс')]]]")
        course3.click()
        assert "true" in course1.get_attribute("aria-selected")
        assert "true" in course3.get_attribute("aria-selected")
        assert "true" in course4.get_attribute("aria-selected")
        search.click()
        time.sleep(3)
        c1, c3, c4, er = 0, 0, 0, 0
        for i in driver.find_elements_by_xpath("//tr/td[8]/div[1]"):
            if i.text == '1':
                c1 += 1
            elif i.text == '3':
                c3 += 1
            elif i.text == '4':
                c4 += 1
            else:
                er += 1
        assert er == 0
        assert c1 >= 1
        assert c3 >= 1
        assert c4 >= 1

    # def test_10(self):  # Фильтрация по условиям обучения. Баг
    #     driver = self.driver
    #     driver.implicitly_wait(10)
    #     driver.find_element_by_xpath("//tr[1]/td[1]/div[1]")
    #     driver.find_element_by_xpath("//button[span[contains(text(), 'Фильтр')]]").click()
    #
    #     condofedu = driver.find_element_by_xpath("//div[label[contains(text(), 'Условия обучения')]]")
    #     condofedu.click()#Открытие списка условий обучения
    #     assert "active" in driver.find_element_by_xpath("//div[div[div[div[div[contains(text(), 'Бюджет')]]]]]").get_attribute("class")
    #     minedu = driver.find_element_by_xpath("//div[div[div[contains(text(), 'Министерство образования')]]]")
    #     minedu.click()
    #     assert "true" in minedu.get_attribute("aria-selected")  # Чекбокс активен
    #     search = driver.find_element_by_xpath("//div[button[span[contains(text(),'Поиск')]]]")
    #     search.click()
    #     time.sleep(3)
    #     for i in driver.find_elements_by_xpath("//tr/td[8]/div[1]"):
    #         assert 'Министерство образования' in i.text

    def test_11(self):  # Фильтрации по признаку наличия и отсутствия стипендии
        driver = self.driver
        driver.implicitly_wait(10)
        driver.find_element_by_xpath("//tr[1]/td[1]/div[1]")
        driver.find_element_by_xpath("//button[span[contains(text(), 'Фильтр')]]").click()
        time.sleep(0.5)


        search = driver.find_element_by_xpath("//div[button[span[contains(text(),'Поиск')]]]")  # Кнопка "Поиск"
        search.click()
        time.sleep(3)
        tgrant1 = driver.find_elements_by_xpath("//tr/td[3]/div[1]/i")
        yes, no, er = 0, 0, 0
        for i in tgrant1:  # Были ли найдены все студенты
            if "plus" in i.get_attribute("class"):
                yes += 1
            elif "minus" in i.get_attribute("class"):
                no += 1
            else:
                er += 1
        assert er == 0
        assert yes >= 1
        assert no >= 1
        driver.find_element_by_xpath("//div[label[contains(text(), 'Есть стипендия?')]]/div/div/button").click() # Очистка поля стипендии
        search.click()
        time.sleep(3)
        assert tgrant1 == driver.find_elements_by_xpath("//tr/td[3]/div[1]/i")

    # def test_12(self):  # Отображение поля условий обучения
    #     driver = self.driver
    #     driver.implicitly_wait(10)
    #     driver.find_element_by_xpath("//tr[1]/td[1]/div[1]")
    #     driver.find_element_by_xpath("//button[span[contains(text(), 'Фильтр')]]").click()
    #
    #     condofedu = driver.find_element_by_xpath("//div[label[contains(text(), 'Условия обучения')]]")
    #     condofedu.click()
    #     assert "active" in driver.find_element_by_xpath("//div[div[div[div[div[contains(text(), 'Бюджет')]]]]]").get_attribute("class")
    #     driver.find_element_by_xpath("//div[div[div[contains(text(), 'Целевой набор')]]]").click()
    #     assert "Целевой набор" == driver.find_element_by_xpath("//div[label[contains(text(), 'Условия обучения')]]/div").text
    #     commerce = driver.find_element_by_xpath("//div[div[div[contains(text(), 'Коммерция')]]]")
    #     commerce.click()
    #     assert "Целевой набор," == driver.find_element_by_xpath("//div[label[contains(text(), 'Условия обучения')]]/div/div[1]").text
    #     assert "Коммерция" == driver.find_element_by_xpath("//div[label[contains(text(), 'Условия обучения')]]/div/div[2]").text
    #     driver.find_element_by_xpath("//div[div[div[contains(text(), 'Министерство образования')]]]").click()
    #     assert "Целевой набор," == driver.find_element_by_xpath("//div[label[contains(text(), 'Условия обучения')]]/div/div[1]").text
    #     assert "Коммерция," == driver.find_element_by_xpath("//div[label[contains(text(), 'Условия обучения')]]/div/div[2]").text
    #     assert "Министерство образования" == driver.find_element_by_xpath("//div[label[contains(text(), 'Условия обучения')]]/div/div[3]").text
    #     driver.find_element_by_xpath("//div[div[div[contains(text(), 'Бюджет')]]]").click()
    #     assert "Целевой набор," == driver.find_element_by_xpath("//div[label[contains(text(), 'Условия обучения')]]/div/div[1]").text
    #     assert "Коммерция," == driver.find_element_by_xpath("//div[label[contains(text(), 'Условия обучения')]]/div/div[2]").text
    #     assert "Министерство образования," == driver.find_element_by_xpath("//div[label[contains(text(), 'Условия обучения')]]/div/div[3]").text
    #     assert "Бюджет" == driver.find_element_by_xpath("//div[label[contains(text(), 'Условия обучения')]]/div/div[4]").text
    #     commerce.click()
    #     assert "Целевой набор," == driver.find_element_by_xpath("//div[label[contains(text(), 'Условия обучения')]]/div/div[1]").text
    #     assert "Министерство образования," == driver.find_element_by_xpath("//div[label[contains(text(), 'Условия обучения')]]/div/div[2]").text
    #     assert "Бюджет" == driver.find_element_by_xpath("//div[label[contains(text(), 'Условия обучения')]]/div/div[3]").text
    #     driver.find_element_by_xpath("//div[div[div[contains(text(), 'Особое право')]]]").click()
    #     assert "Целевой набор," == driver.find_element_by_xpath("//div[label[contains(text(), 'Условия обучения')]]/div/div[1]").text
    #     assert "Министерство образования," == driver.find_element_by_xpath("//div[label[contains(text(), 'Условия обучения')]]/div/div[2]").text
    #     assert "Бюджет," == driver.find_element_by_xpath("//div[label[contains(text(), 'Условия обучения')]]/div/div[3]").text
    #     assert "Особое право" == driver.find_element_by_xpath("//div[label[contains(text(), 'Условия обучения')]]/div/div[4]").text
    #     commerce.click()
    #     assert "Все условия" == driver.find_element_by_xpath("//span[contains(text(), 'Все условия')]").text

    def test_13(self):  # Отображение поля курсов
        driver = self.driver
        driver.implicitly_wait(10)
        driver.find_element_by_xpath("//tr[1]/td[1]/div[1]")
        driver.find_element_by_xpath("//button[span[contains(text(), 'Фильтр')]]").click()

        driver.find_element_by_xpath("//div[label[contains(text(), 'Курс')]]").click()
        assert "active" in driver.find_element_by_xpath("//div[div[div[div[div[contains(text(), '1 курс')]]]]]").get_attribute("class")
        driver.find_element_by_xpath("//div[div[div[contains(text(), '4 курс')]]]").click()
        assert "4 курс" == driver.find_element_by_xpath("//div[label[contains(text(), 'Курс')]]/div/div[1]").text
        course1 = driver.find_element_by_xpath("//div[div[div[contains(text(), '1 курс')]]]")
        course1.click()
        assert "4 курс," == driver.find_element_by_xpath("//div[label[contains(text(), 'Курс')]]/div/div[1]").text
        assert "1 курс" == driver.find_element_by_xpath("//div[label[contains(text(), 'Курс')]]/div/div[2]").text
        driver.find_element_by_xpath("//div[div[div[contains(text(), '3 курс')]]]").click()
        assert "4 курс," == driver.find_element_by_xpath("//div[label[contains(text(), 'Курс')]]/div/div[1]").text
        assert "1 курс," == driver.find_element_by_xpath("//div[label[contains(text(), 'Курс')]]/div/div[2]").text
        assert "3 курс" == driver.find_element_by_xpath("//div[label[contains(text(), 'Курс')]]/div/div[3]").text
        driver.find_element_by_xpath("//div[div[div[contains(text(), '6 курс')]]]").click()
        assert "4 курс," == driver.find_element_by_xpath("//div[label[contains(text(), 'Курс')]]/div/div[1]").text
        assert "1 курс," == driver.find_element_by_xpath("//div[label[contains(text(), 'Курс')]]/div/div[2]").text
        assert "3 курс," == driver.find_element_by_xpath("//div[label[contains(text(), 'Курс')]]/div/div[3]").text
        assert "6 курс" == driver.find_element_by_xpath("//div[label[contains(text(), 'Курс')]]/div/div[4]").text
        driver.find_element_by_xpath("//div[div[div[contains(text(), '5 курс')]]]").click()
        assert "4 курс," == driver.find_element_by_xpath("//div[label[contains(text(), 'Курс')]]/div/div[1]").text
        assert "1 курс," == driver.find_element_by_xpath("//div[label[contains(text(), 'Курс')]]/div/div[2]").text
        assert "3 курс," == driver.find_element_by_xpath("//div[label[contains(text(), 'Курс')]]/div/div[3]").text
        assert "6 курс," == driver.find_element_by_xpath("//div[label[contains(text(), 'Курс')]]/div/div[4]").text
        assert "5 курс" == driver.find_element_by_xpath("//div[label[contains(text(), 'Курс')]]/div/div[5]").text
        course1.click()
        assert "4 курс," == driver.find_element_by_xpath("//div[label[contains(text(), 'Курс')]]/div/div[1]").text
        assert "3 курс," == driver.find_element_by_xpath("//div[label[contains(text(), 'Курс')]]/div/div[2]").text
        assert "6 курс," == driver.find_element_by_xpath("//div[label[contains(text(), 'Курс')]]/div/div[3]").text
        assert "5 курс" == driver.find_element_by_xpath("//div[label[contains(text(), 'Курс')]]/div/div[4]").text
        course1.click()
        driver.find_element_by_xpath("//div[div[div[contains(text(), '2 курс')]]]").click()
        assert "Все курсы" == driver.find_element_by_xpath("//span[contains(text(), 'Все курсы')]").text

if __name__ == '__main__':
    unittest.main()
