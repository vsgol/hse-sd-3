using RabbitMQ.Client;
using System.Text;
namespace logic.Data;

public class QueueUtils
{
    public static void SendMessage(string message)
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
            
            var body = Encoding.UTF8.GetBytes(message);

            var properties = channel.CreateBasicProperties();
            properties.Persistent = true;

            channel.BasicPublish(exchange: "",
                routingKey: "task_queue",
                basicProperties: properties,
                body: body);
            Console.WriteLine(" [x] Queue putted submission {0}", message);
        }
    }
}