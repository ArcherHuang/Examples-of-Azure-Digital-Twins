import { apiHelper } from '../utils/helpers';

export default {
  addTwin(twinName, addTwinJSON) {
    return apiHelper.put(`/api/proxy/digitaltwins/${twinName}?api-version=2020-10-31`, addTwinJSON);
  },
  getTwin(twinId) {
    return apiHelper.get(`/api/proxy/digitaltwins/${twinId}?api-version=2020-10-31`);
  },
  getTwinRelationships(twinId) {
    return apiHelper.get(`/api/proxy/digitaltwins/${twinId}/relationships?api-version=2020-10-31`);
  },
  getTwinInfoById(twinId) {
    return apiHelper.get(`/api/proxy/digitaltwins/${twinId}?api-version=2020-10-31`);
  },
  deleteTwinRelationship(parentId, relationshipId) {
    return apiHelper.delete(`/api/proxy/digitaltwins/${parentId}/relationships/${relationshipId}?api-version=2020-10-31`);
  },
  deleteRpcTwin(twinId) {
    return apiHelper.delete(`/api/proxy/digitaltwins/${twinId}?api-version=2020-10-31`);
  },
  deleteTwin(twinId) {
    return apiHelper.delete(`/api/proxy/digitaltwins/${twinId}?api-version=2020-10-31`);
  },
  addRpcTwin(rpcId, addTwinJSON) {
    return apiHelper.put(`/api/proxy/digitaltwins/${rpcId}?api-version=2020-10-31`, addTwinJSON);
  },
  addRoomRpcRelation(roomId, relationshipId, addTwinJSON) {
    return apiHelper.put(`/api/proxy/digitaltwins/${roomId}/relationships/${relationshipId}?api-version=2020-10-31`, addTwinJSON);
  },
  addRpcTwinXY(twinId, axisX, axisY) {
    return apiHelper.put(`/api/proxy/digitaltwins/${twinId}?api-version=2020-10-31`,
      `
    {
      "$metadata": {
        "$model": "dtmi:itri:cms:perceptor;1",
        "kind": "DigitalTwin"
      },
      "axisX": ${axisX},
      "axisY": ${axisY},
      "threshole5um": 0,
      "threshole3um": 0,
      "threshole1um": 0,
      "threshole05um": 0,
      "timetowatch": 0,
      "timetosleep": 0,
      "rpcAlarm": 0,
      "featureId": 0
    }
    `);
  },
  addRoomTwinXY(twinId) {
    return apiHelper.put(`/api/proxy/digitaltwins/${twinId}?api-version=2020-10-31`,
      `
    {
      "$metadata": {
        "$model": "dtmi:itri:cms:Room;5",
        "kind": "DigitalTwin"
      }
    }
    `);
  },
  addTwinRelation(parentId, relationshipId, addTwinJSON) {
    return apiHelper.put(`/api/proxy/digitaltwins/${parentId}/relationships/${relationshipId}?api-version=2020-10-31`, addTwinJSON);
  },
};
