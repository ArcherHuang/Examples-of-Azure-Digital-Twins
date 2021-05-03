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

                    //{"NEURAL_NETWORK": [
                    // {
                    //  "bbox": [
                    //   0.724,
                    //  0.532,
                    //  0.873,      
                    //  0.649
                    //],
                    //"label": "person",
                    //"confidence": "0.680688",
                    //"timestamp": "1619593595136992992"
                    //}
                    //],
                      // "featureid":19
                    // }
                    var updateTwinData = new JsonPatchDocument();
                    var payload = msg["NEURAL_NETWORK"];
                    if (payload != null)
                    {
                        int counts = 0;
                      
                        long timestamp = 0;
                        long trig = 0;
                        foreach (var s in payload)
                        {
                            var label = s["label"];
                            if (label != null)
                            {
                                string myresult = label.ToString();
                                if (myresult == "person")
                                    counts++;
                            }

                            var time = s["timestamp"];
                            if (time != null)
                            {
                                timestamp = (long)time.Value<long>();
                                trig = timestamp;
                                long time_start = unixTime - trig;
                                log.LogInformation($"trigger time  = :{trig}, in AZF now = :{unixTime}, elaspe = :{time_start}");
                            }
                        }//loop end 
                        updateTwinData.AppendAdd("/pplcount", counts);
                        if (counts >= 10)
                            updateTwinData.AppendAdd("/CrowedAlarm", 1);
                        else
                            updateTwinData.AppendAdd("/CrowedAlarm", 0);
                        if (timestamp != 0)
                            updateTwinData.AppendAdd("/timestamp", timestamp);
                    }

                    //var count = msg["pplcount"];
                    //var alarm = msg["CrowedAlarm"];

                    var roomid = 19;
                   
                    updateTwinData.AppendAdd("/featureId", roomid);
                    

                    if (payload != null)
                    {
                        log.LogInformation($"set property msg:{updateTwinData}");
                        //await client.CreateOrReplaceDigitalTwinAsync(deviceId,updateTwinData);
                        await client.UpdateDigitalTwinAsync(deviceId, updateTwinData);
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
