using System;

class Program
{
    static void Main()
    {
        int frequency = 1000; // 初始频率，单位：赫兹
        int duration = 100;   // 初始时长，单位：毫秒

        Console.WriteLine("使用方向键调整频率和时长，按 Esc 键退出。");

        do
        {
            while (!Console.KeyAvailable)
            {
                Console.Beep(frequency, duration);
            }

            var key = Console.ReadKey(true).Key;

            switch (key)
            {
                case ConsoleKey.UpArrow:
                    frequency += 100;
                    frequency = Math.Min(frequency, 15000); // 限制最大频率
                    break;
                case ConsoleKey.DownArrow:
                    frequency -= 100;
                    frequency = Math.Max(frequency, 37); // 限制最小频率
                    break;
                case ConsoleKey.RightArrow:
                    duration += 10;
                    duration = Math.Min(duration, 1000); // 限制最大时长
                    break;
                case ConsoleKey.LeftArrow:
                    duration -= 10;
                    duration = Math.Max(duration, 10); // 限制最小时长
                    break;
                case ConsoleKey.Escape:
                    return; // 退出程序
            }
        } while (true);
    }
}
