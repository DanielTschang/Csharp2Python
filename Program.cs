using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using System.Net;
using System.Net.Sockets;
using System.Threading;
using System.Text;
using System.IO;
using System.Text.RegularExpressions;


namespace Csharp2Python
{
    class Program
    {
        static void Main(string[] args)
        {

            // SaveDir : 要把抽取出來的keyword存到哪個目錄
            // SearchTitles : Input(要被抽取關鍵字的句子的txt檔)

            string SaveDir = "C:\\Users\\danchang11\\Documents\\GitHub\\5503_chatbot_faq\\data_process\\data\\title_result0607.txt";
            string SearcgTitles = "C:\\Users\\danchang11\\Documents\\GitHub\\5503_chatbot_faq\\data_process\\data\\title.txt";
            Extract(SaveDir,SearchTitles);

        }
        private static string RemoveSymbol(string keyText)
        {
            // 把標點符號濾掉
            string pattern = @"[~!@#\$%\^&\*\(\)\+=\|\\\}\]\{\[:;<,>\?\/""+「【」】，。、]";
            Regex seperatorReg = new Regex(pattern, RegexOptions.IgnorePatternWhitespace);
            keyText = seperatorReg.Replace(keyText, "").Trim();
            return keyText;
        }
        public static string Sendmsg(Socket clientSocket, string sendMessage)
        {
            // 接到目標Socket以及要傳送的String

            byte[] bytes = new byte[1024];
            byte[] msg = Encoding.UTF8.GetBytes(sendMessage);
            int msgLength = msg.Length;

            clientSocket.Send(Encoding.UTF8.GetBytes(msgLength.ToString()));
            clientSocket.Send(msg);

            //Console.WriteLine("向伺服器傳送訊息：" + sendMessage);

            int bytesRec = clientSocket.Receive(bytes);
            string result = Encoding.UTF8.GetString(bytes, 0, bytesRec);

            // Release the socket.


            return result;
        }
        public static void Extract(string SaveDir , string SearchTitles)
        {
            // 這邊定義自己的Socket來接Python回傳的值

            String hostName = Dns.GetHostName();
            IPHostEntry ipHostInfo = Dns.GetHostEntry(hostName);
            IPAddress[] ipAddress = ipHostInfo.AddressList;
            string Tmpip = null;

            foreach (IPAddress ipa in ipAddress)
            {
                if (ipa.AddressFamily == AddressFamily.InterNetwork)
                {
                    Tmpip = ipa.ToString();
                    break;
                }
            }

            IPAddress ip = IPAddress.Parse(Tmpip);
            IPEndPoint remoteEP = new IPEndPoint(ip, 9527);
            // Create a TCP/IP  socket.
            Socket clientSocket = new Socket(ip.AddressFamily, SocketType.Stream, ProtocolType.Tcp);
            try
            {
                clientSocket.Connect(remoteEP);
                Console.WriteLine("連線伺服器成功\n");

            }
            catch
            {
                Console.WriteLine("連線伺服器失敗，請按回車鍵退出！");
            }

            FileStream fs = new FileStream(SaveDir, FileMode.Create);
            StreamWriter sw = new StreamWriter(fs);
            string path = SearchTitles;
            StreamReader sr = new StreamReader(path, Encoding.UTF8);
            string line;
            int a = 0;
            string pattern = @"[~!@#\$%\^&\*\(\)\+=\|\\\}\]\{\[:;<,>\?\/""]+";
            Console.Write(pattern);

            while ((line = sr.ReadLine()) != null)
            {

                string tmp = a.ToString() + ". ";
                line = RemoveSymbol(line);
                Console.Write(line);
                sw.Write(tmp + line+"  ||  ");
                string Receiv = Sendmsg(clientSocket, line);
                sw.Write( Receiv + "\n");
                Console.Write("||" + Receiv+"\n");
                a++;
                Thread.Sleep(350);

            }

            sw.Flush();
            sw.Close();
            string DISCONNECT_MSG = "!DISCONNECT!";
            byte[] DCmsg = Encoding.UTF8.GetBytes(DISCONNECT_MSG);
            int DCmsgLength = DCmsg.Length;

            clientSocket.Send(Encoding.UTF8.GetBytes(DCmsgLength.ToString()));
            clientSocket.Send(DCmsg);
            clientSocket.Shutdown(SocketShutdown.Both);
            clientSocket.Close();

            ;


        }
    }


}
