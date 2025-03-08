import axios from "axios";
import { C } from "../constants";
import { useState } from "react"
import { IformData } from "../interfaces";

const CalcDistance = () => {

  const [distance, setDistance] = useState("");
  const [formData, setFormData] = useState({
    source: "",
    destination: ""
  });
  // const [loading, setLoading] = useState(false);

  const handleDataChange = (e: any) => {

    const name = e.target.name;
    const value = e.target.value;

    let changedData: IformData = formData;

    changedData[name as keyof IformData] = value;
    const temp = Object.assign({}, formData, changedData);
    setFormData(temp);
  }

  const handleSubmitForm = async (e: any) => {
    e.preventDefault();

    // setLoading(true);
    setDistance("Calculating...")

    if (!formData.source) {
      alert("Please enter Source");
      return;
    } else if (!formData.destination) {
      alert("Please enter Destination");
      return;
    }

    const apiRes: any = await sendRequest(formData);
    // setLoading(false);

    if (apiRes.status === 200) {

      setFormData({
        source: apiRes.data.src,
        destination: apiRes.data.dest
      })
      setDistance(apiRes.data.distance);
    } else {
      alert("Something Went Wrong!!!");
      return;
    }
  };

  const sendRequest = async (formData: IformData) => {
    try {

      const data = JSON.stringify(formData);

      var config = {
        method: 'post',
        url: C.backendServiceBaseUrl + 'calc-geometric-distance/',
        headers: { 
          'Content-Type': 'application/json'
        },
        data : data
      };
      
      const resp = await axios(config);
      return resp;
    } catch (err) {
      return;
    }
  }

  return (
    <div>
      <div>
        <label>Source* : </label>
        <input
          type="text"
          name="source"
          value={formData.source}
          placeholder="Enter Start Location"
          onChange={(e) => handleDataChange(e)}
          size={formData.source.length}
        />
      </div>
      <div>
        <label>Destination* : </label>
        <input
          type="text"
          name="destination"
          value={formData.destination}
          placeholder="Enter Destination"
          onChange={(e) => handleDataChange(e)}
          size={formData.destination.length}
        />
      </div>
      <div>
        <button onClick={handleSubmitForm}>Calculate Distance!</button>
        <input
          readOnly
          type="text"
          name="destination"
          placeholder="Distance"
          value={distance}
        />
        kilometers
      </div>
    </div>
  );
}

export default CalcDistance;