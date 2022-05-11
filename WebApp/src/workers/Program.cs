using System;
using System.Diagnostics;
using System.Net;
using RabbitMQ.Client;
using RabbitMQ.Client.Events;
using System.Text;
using System.Threading;
using data_lib;
using logic.Models;


class Worker
{
    public static void Main()
    {
        var folder = Environment.SpecialFolder.LocalApplicationData;
        var path = Environment.GetFolderPath(folder);
        
        using (var webClient = new WebClient())
        using (var db = new HwDbContext())
        {
            var factory = new ConnectionFactory() { HostName = "localhost" };
            using(var connection = factory.CreateConnection())
            using(var channel = connection.CreateModel())
            {
                channel.QueueDeclare(queue: "task_queue",
                    durable: true,
                    exclusive: false,
                    autoDelete: false,
                    arguments: null);

                channel.BasicQos(prefetchSize: 0, prefetchCount: 1, global: false);

                Console.WriteLine(" [*] Waiting for messages.");

                var consumer = new EventingBasicConsumer(channel);
                consumer.Received += (sender, ea) =>
                {
                    var body = ea.Body.ToArray();
                    var message = Encoding.UTF8.GetString(body);
                    Console.WriteLine(" [x] Received attempt id {0}", message);
                    
                    int id = Int32.Parse(message);

                    Attempt attempt = db.Attempts.Find(id);
                    if (attempt == null)
                        Console.WriteLine($" [x] FAILED TO FIND SUBMISSION");
                    else
                    {
                        try
                        {
                            Console.WriteLine($" [x] Link: {attempt.Link}");
                            string filePath = Path.Join(path, "HwProjSubmissions");

                            Directory.CreateDirectory(filePath);

                            filePath = Path.Join(filePath, $"{attempt.Id}");
                            
                            webClient.DownloadFile(attempt.Link, filePath);

                            
                            Process p = new Process();
                            p.StartInfo.UseShellExecute = false;
                            p.StartInfo.RedirectStandardOutput = true;
                            p.StartInfo.FileName = "check.sh";
                            p.StartInfo.Arguments = $"{filePath} {attempt.Link} {attempt.SubmissionDate} {attempt.TaskId}";
                            p.Start();
                            string output = p.StandardOutput.ReadToEnd();
                            p.WaitForExit();
                            attempt.Output = output;
                        }
                        catch (Exception e)
                        {
                            attempt.Output = "Failed to check. Error message:\n" + e.Message;
                        }
                    }

                    db.SaveChanges();
                    Console.WriteLine(" [x] Done");

                    channel.BasicAck(deliveryTag: ea.DeliveryTag, multiple: false);
                };
                channel.BasicConsume(queue: "task_queue",
                    autoAck: false,
                    consumer: consumer);

                Console.WriteLine(" Press [enter] to exit.");
                Console.ReadLine();
            }
        }
    }
}