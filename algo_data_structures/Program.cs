
using System;
using System.Diagnostics;
using System.Numerics;

namespace Projekt3
{
    internal class Program
    {
        static sorts sort  = new sorts();
        static int[] t = new int[50000];
        const int NIter = 3; // FOR QUICK SORT
        //const int NIter = 1; // FOR BASIC SORT
        const int Consta = 5;
        static Random rnd = new Random(Guid.NewGuid().GetHashCode());
        static void GenerateAscendingArray(int[] t)
        {
            for (int i = 0; i < t.Length; ++i) t[i] = i;
            //return t;
        }
        static void GenerateDescendingArray(int[] t)
        {
            for (int i = 0; i < t.Length; ++i) t[i] = t.Length - i - 1;
            //return t;
        }
        static void GenerateVShape(int[] t)
        {
            int n = t.Length;
            int middle = n / 2;
            for (int i = 0; i < middle; i++)
            {
                t[i] = n - 1 - (i * 2);
            }
            for (int i = middle; i < n; i ++)
            {
                t[i] = (i - middle) * 2;
            }
            //return t;
        }
        static void GenerateAShape(int[] t)
        {
            int n = t.Length;
            int middle = n / 2;
            for (int i = 0; i < middle; i++)
            {
                t[i] = i * 2;
            }
            for (int i = middle; i < n; i++)
            {
                t[i] = n - 1 - (i - middle) * 2;
            }
            //return t;
        }
        static void GenerateRandomArray(int[] t, Random rnd, int maxValue = int.MaxValue)
        {
            for (int i = 0; i < t.Length; ++i)
                t[i] = rnd.Next(maxValue);
        }

        static void GenerateConst(int[] t)
        {
            for (int i = 0; i < t.Length; i++)
            {
                t[i] = Consta;
            }
        }
        static string SortTimeQuick(int c, int[] t) //TIME FOR QUICKSORT WITH DIFFRENT PIVOT VALUES
        {
            double ElapsedSeconds;
            long ElapsedTime = 0, MinTime = long.MaxValue, MaxTime = long.MinValue, IterationElapsedTime;

            for (int i = 0; i < (NIter + 2); ++i)
            {

                long start = Stopwatch.GetTimestamp();
                sort.qsort_it(t, c);
                long end = Stopwatch.GetTimestamp();
                IterationElapsedTime = end - start;
                ElapsedTime += IterationElapsedTime;
                if (IterationElapsedTime > MaxTime) MaxTime = IterationElapsedTime;
                if (IterationElapsedTime < MinTime) MinTime = IterationElapsedTime;
            }
            ElapsedTime -= MaxTime + MinTime;
            ElapsedSeconds = ElapsedTime * (1.0 / (NIter * Stopwatch.Frequency));
            Console.Write("\t" + ElapsedSeconds.ToString("F10"));
            return ElapsedSeconds.ToString("F10");
        }
        static string SortTime(int c,int[] t)
        {
            double ElapsedSeconds;
            long ElapsedTime = 0, MinTime = long.MaxValue, MaxTime = long.MinValue, IterationElapsedTime;

            for (int i = 0; i < (NIter + 2); ++i)
            {

                long start = Stopwatch.GetTimestamp();
                SortChoose(c,t); //METODA DO WYBIERANIA SORTOWANIA ZAMIAST JEDNEJ KONKRETNEJ
                long end = Stopwatch.GetTimestamp();
                IterationElapsedTime = end - start;
                ElapsedTime += IterationElapsedTime;
                if (IterationElapsedTime > MaxTime) MaxTime = IterationElapsedTime;
                if (IterationElapsedTime < MinTime) MinTime = IterationElapsedTime;
            }
            ElapsedTime -= MaxTime + MinTime;
            ElapsedSeconds = ElapsedTime * (1.0 / (NIter * Stopwatch.Frequency));
            Console.Write("\t" + ElapsedSeconds.ToString("F10"));
            return ElapsedSeconds.ToString("F10");
        }
        static void SortChoose(int c, int[] t)
        {
            switch (c)
            {
                case 0:
                    //Console.WriteLine("HeapSort");
                    sort.HeapSort(t);
                    break;
                case 1:
                   // Console.WriteLine("CocktaSort");
                    sort.CocktailSort(t);
                    break;
                case 2:
                    //Console.WriteLine("InsertionSort");
                    sort.InsertionSort(t);
                    break;
                case 3:
                    //Console.WriteLine("SelectionSort");
                    sort.SelectionSort(t);
                    break;
                case 4:
                    sort.qsort(t, 0, t.Length - 1);
                    break;
                case 5:
                    sort.qsort_it(t, 0);
                    break;
                default:
                    break;
            }
        }
        static string TableChoose(int c)
        {
            switch (c)
            {
                case 0:
                    return "Desc";  
                case 1:
                    return "Ascd";
                case 2:
                    return "Rand";
                case 3:
                    return "V-sh";                 
                case 4:
                    return "Const";
                default:
                    return "";
            }
        }
        static void GenChoose(int c, int[] t)
        {
            switch (c)
            {
                case 0:
                    GenerateDescendingArray(t);
                    break;
                case 1:
                    GenerateAscendingArray(t);
                    break;
                case 2:
                    GenerateRandomArray(t, rnd);
                    break;
                case 3:
                    GenerateVShape(t);
                    break;
                case 4:
                    GenerateConst(t);
                    break;
                default:
                    break;
            }
        }
        static void BasicSorts()
        {
            Console.WriteLine("\t\tTIME ANALYSIS 4 DIFFRENT SORT ALGORITHMS");
            //Console.WriteLine("Table\tHeapSort\t CoctailSort\t InsertionSort \t SelectionSort");
            using (StreamWriter writer = new StreamWriter("C:\\Users\\jakob\\OneDrive\\Pulpit\\c#\\Algorytmy\\Projekt3\\results.txt"))
            {
                for (int i = 10000; i < 85001; i += 5000)
                {
                    int[] x = new int[i];
                    
                    Console.Write("\n\nTable\tArray\tHeapSort\t CoctailSort\t InsertionSort \t SelectionSort");
                    //Console.Write("\n" + x.Length);
                    //writer.Write(x.Length + ";");
                    for (int j = 0; j < 5; j++)
                    {                       
                        Console.Write("\n" + x.Length + "\t" + TableChoose(j));
                        writer.Write("\n" + x.Length + ";" + TableChoose(j) + ";");
                        for (int z = 0; z < 4; z++)
                        {
                            GenChoose(j, x); // PĘTLA FOR DLA ROZNYCH ROZMIAROW TABLIC TU MUSISZ ZROBIĆ
                                             //foreach (int item in t) Console.Write(" " + item);
                            writer.Write(SortTime(z, x) + ";");
                        }
                    }
                }
            }
        }
        static void QuickSortI()
        {
            Console.Write("\n\n");
            Console.WriteLine("  TIME ANALYSIS 2 QUICK SORTS FOR RAND ARRAY");
            Console.WriteLine("ARRAY\t RECURSIVE\tDIY STACK");
            using (StreamWriter writer = new StreamWriter("C:\\Users\\jakob\\OneDrive\\Pulpit\\c#\\Algorytmy\\Projekt3\\results_quick.txt"))
            {
                for (int i = 50000; i < 200001; i += 10000) //CZY DLA RÓŻNYCH TABLIC CZY JEDNEJ ROZMIAR TABLICY?   
                {
                    int[] x = new int[i];
                    Console.Write(x.Length);
                    writer.Write(x.Length + ";");
                    for (int j = 4; j < 6; j++)
                    {
                        GenerateRandomArray(x, rnd);
                        writer.Write(SortTime(j, x) + ";");
                    }
                    writer.Write('\n');
                    Console.Write("\n");
                }
            }
        }
        static void QuickSortIIKey()
        {
            Console.Write("\n");
            Console.WriteLine("QUICK SORT WITH DIFFRENT KEY ANALYSIS");
            Console.WriteLine("Table\tMedian\t\tExtremeRight\tRandomPivot");
            using (StreamWriter writer = new StreamWriter("C:\\Users\\jakob\\OneDrive\\Pulpit\\c#\\Algorytmy\\Projekt3\\results_pivot_key.txt"))
            {
                for (int i = 50000; i < 100001; i += 5000) //CZY DLA RÓŻNYCH TABLIC CZY JEDNEJ ROZMIAR TABLICY?
                {
                    int[] x = new int[i];
                    writer.Write(x.Length);
                    Console.Write(x.Length);
                    for (int j = 0; j < 3; j++)
                    {
                        GenerateDescendingArray(x);
                        writer.Write(";" + SortTimeQuick(j, x));
                    }
                    Console.Write("\n");
                    writer.Write('\n');
                }
            }
        }
        static void Tester() // QUICK SORT //
        {
            QuickSortI(); // BADANIE 1 częsci polecenia III
            QuickSortIIKey(); // BADANIE 2 częsci polecenia III
        }
        static void Main(string[] args)
        {
            BasicSorts(); //BADANIE I, II polecenia TABLICE [50 - 200k] W PĘTLI
            /////////////////////////////// QUICK SORT //////////////////////////////////////
            Thread TesterThread = new Thread(Program.Tester, 8 * 1024 * 1024); // utworzenie wątku
            TesterThread.Start(); // uruchomienie wątku
            TesterThread.Join(); // oczekiwanie na zakończenie wątku

        }
    }
}
