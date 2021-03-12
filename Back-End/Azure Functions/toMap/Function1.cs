// Default URL for triggering event grid function in the local environment.
// http://localhost:7071/runtime/webhooks/EventGrid?functionName={functionname}
using System;
using Microsoft.Azure.WebJobs;
using Microsoft.Azure.WebJobs.Host;
using Microsoft.Azure.EventGrid.Models;
using Microsoft.Azure.WebJobs.Extensions.EventGrid;
using Microsoft.Extensions.Logging;
using Newtonsoft.Json;
using Newtonsoft.Json.Linq;
using System.Threading.Tasks;
using System.Net.Http;

namespace toMap
{
    public static class Function1
    {
        //Read maps credentials from application settings on function startup
        private static string statesetID = Environment.GetEnvironmentVariable("statesetID");
        private static string subscriptionKey = Environment.GetEnvironmentVariable("subscription-key");
        private static HttpClient httpClient = new HttpClient();
        [FunctionName("Function1")]
        public static async Task Run([EventGridTrigger]EventGridEvent eventGridEvent, ILogger log)
        {
            log.LogInformation(eventGridEvent.Data.ToString());
            JObject message = (JObject)JsonConvert.DeserializeObject(eventGridEvent.Data.ToString());
            log.LogInformation("Reading event from twinID:" + eventGridEvent.Subject.ToString() + ": " +
                eventGridEvent.EventType.ToString() + ": " + message["data"]);

            //Parse updates to "space" twins
            if (message["data"]["modelId"].ToString() == "dtmi:itri:cms:RPCstat;9")
            {   //Set the ID of the room to be updated in your map. 
                //Replace this line with your logic for retrieving featureID. 


                string featureID = "UNIT";
                log.LogInformation("statesetID " + statesetID);
                //Iterate through the properties that have changed
                foreach (var operation in message["data"]["patch"])
                {
                    if(operation["op"].ToString() == "add" && operation["path"].ToString() == "/featureId")
                    {
                        featureID = featureID + operation["value"].ToString();
                        log.LogInformation("feature id " + featureID);
                    }

                    var timeSpan = (DateTime.UtcNow - new DateTime(1970, 1, 1, 0, 0, 0));
                    long unixTime = (long)timeSpan.TotalSeconds;

                    long trig = 0;
                    if (operation["op"].ToString() == "add" && operation["path"].ToString() =="/timestamp")
                    {
                        trig = operation["value"].Value<long>();
                        long time_start = unixTime - trig;
                        log.LogInformation($"device trigger time  = :{trig}, in to Map AZF now = :{unixTime}, elaspe = :{time_start}");
                    }

                    if (operation["op"].ToString() == "add" && operation["path"].ToString() == "/rpcAlarm" && featureID.Length > 4)
                    {   //Update the maps feature stateset
                        
                        var val = operation["value"].Value<int>();
                        var setAlarm = "no";
                        if (val == -1)
                            setAlarm = "no";
                        else if (val == 1)
                            setAlarm = "alarm";
                        else
                            setAlarm = "normal";

                        var postcontent = new JObject(new JProperty("States", new JArray(
                            new JObject(new JProperty("keyName", "setAlarm"),
                                 new JProperty("value", setAlarm.ToString()),
                                 new JProperty("eventTimestamp", DateTime.Now.ToString("s"))))));

                        var response = await httpClient.PostAsync(
                            $"https://atlas.microsoft.com/featureState/state?api-version=1.0&statesetID={statesetID}&featureID={featureID}&subscription-key={subscriptionKey}",
                            new StringContent(postcontent.ToString()));

                        log.LogInformation(await response.Content.ReadAsStringAsync());

                        //if (operation["op"].ToString() == "add" && operation["path"].ToString() == "/timestamp")
                        {
                        //    trig = operation["value"].Value<long>();
                           timeSpan = (DateTime.UtcNow - new DateTime(1970, 1, 1, 0, 0, 0));
                            unixTime = (long)timeSpan.TotalSeconds;
                            //long time_start = unixTime - trig;
                           log.LogInformation($"device trigger time  = :{trig}, out Map AZF now = :{unixTime}");
                           // log.LogInformation($"device trigger time  = :{trig}, out Map AZF now = :{unixTime}, elaspe = :{time_start}");
                        }
                    }
                }
            }
        }
    }
}
