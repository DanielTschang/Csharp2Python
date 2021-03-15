using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using System.Net;
using System.Net.Sockets;
using System.Threading;
using System.Text;

namespace Csharp2Python
{
    class Program
    {
        static void Main(string[] args)
        {
            string SendMessage = "若是在夜間或其他時間遭到家庭暴力";
            string tmp = Extract(SendMessage);

            Console.Write("結果");
            Console.WriteLine(tmp);

            ;
        }
        public static string Sendmsg(Socket clientSocket, string sendMessage)
        {
            byte[] bytes = new byte[1024];
            byte[] msg = Encoding.UTF8.GetBytes(sendMessage);
            int msgLength = msg.Length;

            clientSocket.Send(Encoding.UTF8.GetBytes(msgLength.ToString()));
            clientSocket.Send(msg);

            Console.WriteLine("向伺服器傳送訊息：" + sendMessage);

            int bytesRec = clientSocket.Receive(bytes);
            string result = Encoding.UTF8.GetString(bytes, 0, bytesRec);

            string DISCONNECT_MSG = "!DISCONNECT!";
            byte[] DCmsg = Encoding.UTF8.GetBytes(DISCONNECT_MSG);
            int DCmsgLength = DCmsg.Length;

            clientSocket.Send(Encoding.UTF8.GetBytes(DCmsgLength.ToString()));
            clientSocket.Send(DCmsg);


            // Release the socket.  
            clientSocket.Shutdown(SocketShutdown.Both);
            clientSocket.Close();

            return result;
        }
        public static string Extract(string SendMessage)
        {
            String hostName = Dns.GetHostName();
            IPHostEntry ipHostInfo = Dns.GetHostEntry(hostName);
            IPAddress[] ipAddress = ipHostInfo.AddressList;
            string Tmpip = null;
            string fake = "error";

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
                Console.WriteLine("連線伺服器成功");

            }
            catch
            {
                Console.WriteLine("連線伺服器失敗，請按回車鍵退出！");
                return fake;
            }
            return Sendmsg(clientSocket, SendMessage);

            
        }
    }
}
