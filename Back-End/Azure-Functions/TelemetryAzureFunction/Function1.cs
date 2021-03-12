// Default URL for triggering event grid function in the local environment.
// http://localhost:7071/runtime/webhooks/EventGrid?functionName={functionname}
using System;

using Microsoft.Azure.WebJobs;
using Microsoft.Azure.WebJobs.Host;
using Microsoft.Azure.EventGrid.Models;
using Microsoft.Azure.WebJobs.Extensions.EventGrid;
using Microsoft.Extensions.Logging;
using Azure.DigitalTwins.Core;
using Azure.DigitalTwins.Core.Serialization;
using Azure.Identity;
using System.Net.Http;
using Azure.Core.Pipeline;
using Newtonsoft.Json;
using Newtonsoft.Json.Linq;
using Azure;


namespace FunctionAppDigitalTwins
{
   
    public class Function1
    {
        private static readonly string adtInstanceUrl = Environment.GetEnvironmentVariable("ADT_SERVICE_URL");
        private static readonly HttpClient httpClient = new HttpClient();
        [FunctionName("TwinsFunction")]
        public async void Run([EventGridTrigger]EventGridEvent eventGridEvent, ILogger log)
        {
            if (adtInstanceUrl == null) log.LogError("Application setting \"ADT_SERVICE_URL\" not set");

            try
            {
                //Authenticate with Digital Twins
                ManagedIdentityCredential cred = new ManagedIdentityCredential("https://digitaltwins.azure.net");
                DigitalTwinsClient client = new DigitalTwinsClient(
                    new Uri(adtInstanceUrl), cred, new DigitalTwinsClientOptions
                    { Transport = new HttpClientTransport(httpClient) });
                log.LogInformation($"ADT service client connection created.");

                if (eventGridEvent != null && eventGridEvent.Data != null)
                {
                    log.LogInformation(eventGridEvent.Data.ToString());

                    // Reading deviceId and temperature for IoT Hub JSON
                    JObject deviceMessage = (JObject)JsonConvert.DeserializeObject(eventGridEvent.Data.ToString());
                    string deviceId = (string)deviceMessage["systemProperties"]["iothub-connection-device-id"];
                    var msg = deviceMessage["body"];
                    var um5 = msg["particle5um"];
                    var um3 = msg["particle3um"];
                    var um1 = msg["particle1um"];
                    var um05 = msg["particle05um"];
                    log.LogInformation($"Device:{deviceId} rpc 5 um is:{um5}");
                    log.LogInformation($"Device:{deviceId} rpc 3 um is:{um3}");
                    log.LogInformation($"Device:{deviceId} rpc 1 um is:{um1}");
                    log.LogInformation($"Device:{deviceId} rpc 0.5 um is:{um05}");
                    
                    //var temperature = deviceMessage["body"]["temperature"];
                    //log.LogInformation($"Device:{deviceId} temperature is:{msg}");
                    //log.LogInformation($"Device:{deviceId} RPC is:{msg}");

                    //Update twin using device temperature
                    var updateTwinData = new JsonPatchDocument();
                    updateTwinData.AppendReplace("/setTarget5um", um5.Value<long>());
                    //updateTwinData.AppendReplace("/um3", um3.Value<long>());
                    //updateTwinData.AppendReplace("/um1", um1.Value<long>());
                    //updateTwinData.AppendReplace("/um05", um05.Value<long>());
                    //await client.PublishTelemetryAsync(twinId, Guid.NewGuid().ToString(), "{\"um5\": 5}");
                    await client.UpdateDigitalTwinAsync(deviceId, updateTwinData);
                }
            }
            catch (Exception e)
            {
                log.LogError($"Error in ingest function: {e.Message}");
            }
        }
    }
}
