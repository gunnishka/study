using System;

namespace ATM
{
    class Program
    {
        static int[] values = {5000, 2000, 1000, 500, 200, 100};
        static void Main()
        {
            Console.Write("Введите сумму к выводу: \n");
            string input = Console.ReadLine();
            int n = Convert.ToInt32(input);
            if (n <= 150000 && n % 100 == 0)
            {
                giveValues(n);
            }
            else
            {
                Console.Write("Сумма должна быть меньше 150.000 и кратна 100 \n");
            }
        }

        static void giveValues(int n)
        {
            int[] counterOfOperations = new int[values.Length];
            int remain = n;
            for (int i=0; i < values.Length; i++)
            {
                if (remain >= values[i])
                {
                    counterOfOperations[i] = remain / values[i];
                    remain %= values[i];
                }
                if (counterOfOperations[i] != 0)
                {
                    Console.Write($"Купюры номиналом: {values[i]} в количестве: {counterOfOperations[i]}\n");
                }                
            }
        }
    }
}