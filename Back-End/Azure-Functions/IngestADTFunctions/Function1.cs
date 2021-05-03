// Default URL for triggering event grid function in the local environment.
// http://localhost:7071/runtime/webhooks/EventGrid?functionName={functionname}
using System;
using Microsoft.Azure.WebJobs;
using Microsoft.Azure.WebJobs.Host;
using Microsoft.Azure.EventGrid.Models;
using Microsoft.Azure.WebJobs.Extensions.EventGrid;
using Microsoft.Extensions.Logging;
using Azure.DigitalTwins.Core;
//using Azure.DigitalTwins.Core.Serialization;
using Azure.Identity;
using System.Net.Http;
using Azure.Core.Pipeline;
using Newtonsoft.Json;
using Newtonsoft.Json.Linq;
using Azure;
namespace IngestADTFunctions
{
    public class Function1
    {
        private static readonly string adtInstanceUrl = Environment.GetEnvironmentVariable("ADT_SERVICE_URL");
        
        private static readonly HttpClient httpClient = new HttpClient();
        [FunctionName("Function1")]
        public async void Run([EventGridTrigger]EventGridEvent eventGridEvent, ILogger log)
        {
            log.LogInformation(adtInstanceUrl);
            if (adtInstanceUrl == null) log.LogError("Application setting \"ADT_SERVICE_URL\" not set");

            //log.LogInformation(eventGridEvent.Data.ToString());
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
                    var timeSpan = (DateTime.UtcNow - new DateTime(1970, 1, 1, 0, 0, 0));
                    long unixTime = (long)timeSpan.TotalSeconds;

                    // Reading deviceId and temperature for IoT Hub JSON
                    JObject deviceMessage = (JObject)JsonConvert.DeserializeObject(eventGridEvent.Data.ToString());
                    log.LogInformation($"Device msg:{deviceMessage}");
                    string deviceId = (string)deviceMessage["systemProperties"]["iothub-connection-device-id"];
                    string componetid = (string)deviceMessage["systemProperties"]["dt-subject"];
                    var msg = deviceMessage["body"];
                    var count = msg["pplcount"];
                    var alarm = msg["CrowedAlarm"];
                    var roomid = msg["featureId"];
                    var timestamp = msg["timestamp"];

                    long trig = 0;
                    if (timestamp != null)
                    {
                        trig = timestamp.Value<long>();
                        long time_start = unixTime - trig;
                        log.LogInformation($"trigger time  = :{trig}, in AZF now = :{unixTime}, elaspe = :{time_start}");
                    }

                    //Update twin using device temperature
                    var updateTwinData = new JsonPatchDocument();

                    if (alarm != null)
                    {
                        updateTwinData.AppendAdd("/pplcount", count.Value<long>());
                        updateTwinData.AppendAdd("/featureId", roomid.Value<int>());
                        if (count != null)
                        {
                            if (count.Value<long>() >= 10)
                                alarm = 1;
                            updateTwinData.AppendAdd("/CrowedAlarm", alarm.Value<int>());
                            if (timestamp != null)
                                updateTwinData.AppendAdd("/timestamp", timestamp.Value<long>());
                            log.LogInformation($"set property msg:{updateTwinData}");
                            //await client.CreateOrReplaceDigitalTwinAsync(deviceId,updateTwinData);
                            await client.UpdateDigitalTwinAsync(deviceId, updateTwinData);
                        }


                        if (timestamp != null)
                        {
                            timeSpan = (DateTime.UtcNow - new DateTime(1970, 1, 1, 0, 0, 0));
                            unixTime = (long)timeSpan.TotalSeconds;

                            trig = timestamp.Value<long>();
                            long time_end = unixTime - trig;
                            log.LogInformation($"trigger time  = :{trig}, to ADT now = :{unixTime}, elaspe = :{time_end}");

                        }
                    }
                }
            }
            catch (Exception e)
            {
                log.LogError($"ADT Error in ingest function: {e.Message}");
            }
        }
    }
}
