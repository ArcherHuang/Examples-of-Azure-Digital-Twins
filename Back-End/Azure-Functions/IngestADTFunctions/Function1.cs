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
                    //log.LogInformation($"Device msg:{deviceMessage}");
                    string deviceId = (string)deviceMessage["systemProperties"]["iothub-connection-device-id"];
                    string componetid = (string)deviceMessage["systemProperties"]["dt-subject"];
                    var msg = deviceMessage["body"];
                    var um5 = msg["particle5um"];
                    var um3 = msg["particle3um"];
                    var um1 = msg["particle1um"];
                    var um05 = msg["particle05um"];
                    var alarm = msg["rpcAlarm"];
                    var roomid = msg["featureId"];
                    var timestamp = msg["timestamp"];

                    long trig = 0;
                    if(timestamp != null)
                    {
                        trig = timestamp.Value<long>();
                        long time_start = unixTime - trig;
                        log.LogInformation($"trigger time  = :{trig}, in AZF now = :{unixTime}, elaspe = :{time_start}");
                    }

                    //Update twin using device temperature
                    var updateTwinData = new JsonPatchDocument();
                    if (alarm != null)
                    {
                        //updateTwinData.AppendReplace("/particle5um", um5.Value<long>());
                        //updateTwinData.AppendReplace("/particle3um", um3.Value<long>());
                        //updateTwinData.AppendReplace("/particle1um", um1.Value<long>());
                        //updateTwinData.AppendReplace("/particle05um", um05.Value<long>());
                        //if (alarm != null)
                        //    updateTwinData.AppendReplace("/rpcAlarm", alarm.Value<int>());


                        updateTwinData.AppendAdd("/particle5um", um5.Value<long>());
                        updateTwinData.AppendAdd("/particle3um", um3.Value<long>());
                        updateTwinData.AppendAdd("/particle1um", um1.Value<long>());
                        updateTwinData.AppendAdd("/particle05um", um05.Value<long>());
                        updateTwinData.AppendAdd("/featureId", roomid.Value<int>());
                        if (alarm != null)
                            updateTwinData.AppendAdd("/rpcAlarm", alarm.Value<int>());

                        if (timestamp != null)
                            updateTwinData.AppendAdd("/timestamp", timestamp.Value<long>());
                        log.LogInformation($"set property msg:{updateTwinData}");
                        //await client.CreateOrReplaceDigitalTwinAsync(deviceId,updateTwinData);
                        await client.UpdateDigitalTwinAsync(deviceId, updateTwinData);
                    }
                    
                    var threshole5um = msg["threshole5um"];
                    var threshole3um = msg["threshole3um"];
                    var threshole1um = msg["threshole1um"];
                    var threshole05um = msg["threshole05um"];
                    var timetowatch = msg["timetowatch"];
                    var timetosleep = msg["timetosleep"];

                    var configurationTwinData = new JsonPatchDocument();
                    if (threshole05um != null)
                    {
                        configurationTwinData.AppendAdd("/threshole5um", threshole5um.Value<long>());
                        configurationTwinData.AppendAdd("/threshole3um", threshole3um.Value<long>());
                        configurationTwinData.AppendAdd("/threshole1um", threshole1um.Value<long>());
                        configurationTwinData.AppendAdd("/threshole05um", threshole05um.Value<long>());
                        configurationTwinData.AppendAdd("/timetowatch", timetowatch.Value<int>());
                        configurationTwinData.AppendAdd("/featureId", roomid.Value<int>());
                        configurationTwinData.AppendAdd("/timetosleep", timetosleep.Value<int>());
                        if (timestamp != null)
                            updateTwinData.AppendAdd("/timestamp", timestamp.Value<long>());

                        //configurationTwinData.AppendReplace("/threshole5um", threshole5um.Value<long>());
                        //configurationTwinData.AppendReplace("/threshole3um", threshole3um.Value<long>());
                        //configurationTwinData.AppendReplace("/threshole1um", threshole1um.Value<long>());
                        //configurationTwinData.AppendReplace("/threshole05um", threshole05um.Value<long>());
                        //configurationTwinData.AppendReplace("/timetowatch", timetowatch.Value<int>());
                        //configurationTwinData.AppendReplace("/timetosleep", timetosleep.Value<int>());
                        log.LogInformation($"configuration  msg:{configurationTwinData}");
                        //await client.CreateOrReplaceDigitalTwinAsync(deviceId, configurationTwinData);
                        await client.UpdateDigitalTwinAsync(deviceId, configurationTwinData);

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
            catch (Exception e)
            {
                log.LogError($"ADT Error in ingest function: {e.Message}");
            }
        }
    }
}
