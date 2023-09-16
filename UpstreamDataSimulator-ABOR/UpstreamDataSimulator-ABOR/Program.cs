using System;
using System.Collections.Generic;
using System.IO;
using CsvHelper;
using Azure.Storage.Blobs;
using System.Timers; // Add this line
using Timer = System.Timers.Timer;

namespace UpstreamDataSimulator_ABOR
{


    class Program
    {





        public static void Main(string[] args)
        {
            Timer timer = new Timer(120000); // Set the timer to trigger every 2 minutes
            timer.Elapsed += GenerateAndUploadFile;
            timer.Start();

            Console.WriteLine("Press any key to stop...");
            Console.ReadKey();
        }

        private static void GenerateAndUploadFile(Object source, ElapsedEventArgs e)
        {
            var random = new Random();
            var funds = new List<string> { "Fund1", "Fund2", "Fund3", "Fund4", "Fund5" }; // Add more fund IDs as needed
            var securities = new List<string> { "APPLE", "MICROSOFT", "GOOGLE", "AMAZON", "FACEBOOK" }; // Add more security IDs as needed
            var positions = new List<Position>();

            for (int i = 0; i < 100; i++)
            {
                var position = new Position
                {
                    SecurityId = securities[random.Next(securities.Count)],
                    AsOfDate = DateTime.Now.AddDays(random.Next(-365, 365)).ToString("MM/dd/yyyy"), // Format the date here,
                    FundId = funds[random.Next(funds.Count)],
                    Quantity = random.Next(1, 1000),
                    MarketValue = random.Next(1, 10000) + random.NextDouble()
                };

                positions.Add(position);
            }

            string timestamp = DateTime.Now.ToString("yyyyMMddHHmmss");
            string filePath = $"SecurityPositions_{timestamp}.csv";
            using (var writer = new StreamWriter(filePath))
            using (var csv = new CsvWriter(writer, System.Globalization.CultureInfo.InvariantCulture))
            {
                csv.WriteRecords(positions);
            }

            // Upload the file to Azure Blob Storage
            string connectionString = "DefaultEndpointsProtocol=https;AccountName=aabbdatalake2023;AccountKey=9aMOMwRaBw3gm7TrODl/+5N6nQIJ7RHEGIXhnPqUrL7QjeLlXOU2MsvrpVR1EpE5Yr3D7foXxjrw+AStRdhCGg==;EndpointSuffix=core.windows.net"; // Replace with your Azure Storage connection string
            string containerName = "container-src-1"; // Replace with your Blob container name
            BlobServiceClient blobServiceClient = new BlobServiceClient(connectionString);
            BlobClient blobClient = blobServiceClient.GetBlobContainerClient(containerName).GetBlobClient(Path.GetFileName(filePath));

            using (FileStream uploadFileStream = File.OpenRead(filePath))
            {
                blobClient.Upload(uploadFileStream, true);
                uploadFileStream.Close();
            }

            Console.WriteLine($"File generated and uploaded at: {DateTime.Now}");
        }


        public class Position
        {
            public string SecurityId { get; set; }
            public string AsOfDate { get; set; }
            public string FundId { get; set; }
            public int Quantity { get; set; }
            public double MarketValue { get; set; }
        }
    }
}
