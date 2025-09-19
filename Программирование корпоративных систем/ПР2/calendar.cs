using System;

namespace Calendar
{
    class Program
    {
        static void Main()
        {
            int startday;
            while (true)
            {
                Console.Write("Введите номер дня недели для первого мая (1-пн, 2-вт..., 7-вс): \n");
                if (int.TryParse(Console.ReadLine(), out startday) && startday >= 1 && startday <= 7)
                {
                    break;
                }
                else
                {
                    Console.Write("Ошибка! Введите число от 1 до 7: \n");
                }
            }

            while (true)
            {
                Console.Write("Введите число для проверки (1-31) или '0' для выхода: \n");
                string input = Console.ReadLine();
                if (input == "0")
        {   
                    break;
                }
                if (int.TryParse(input, out int day) && day >= 1 && day <= 31)
                {
                    Console.Write("----Проверяем выходной ли день---- \n");
                    CheckDayType(day, startday);
                }
                else
                {
                    Console.Write("Ошибка! Введите число от 1 до 31: \n");
                }
            }
        }

        static void CheckDayType(int day, int startday)
        {
            int dayOfWeek = (startday + day - 2) % 7 + 1;

            bool isWeekend = (dayOfWeek == 6 || dayOfWeek == 7);
            bool isHoliday = (day >= 1 && day <= 5) || (day <= 10 && day >= 8);

            string dayName = getDayOfWeekName(dayOfWeek);

            Console.Write($"{day} мая - {dayName}\n");

            if (isWeekend || isHoliday)
            {
                Console.Write("Выходной день \n");
            }
            else
            {
                Console.Write("Рабочий день \n");
            }
        }

        static string getDayOfWeekName(int dayNumber)
        {
            return dayNumber switch
            {
                1 => "понедельник",
                2 => "вторник",
                3 => "среда",
                4 => "четверг",
                5 => "пятница",
                6 => "суббота",
                7 => "воскресенье",
                _ => "неизвестный день"
            };
        }
    }
}