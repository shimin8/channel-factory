import axios from "axios";
import { C } from "../constants";
import { useState } from "react"
import { IformData } from "../interfaces";
import '../App.css'

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

    if (!formData.source || !formData.destination) {
      alert("Source and Destination are mandatory fields!");
      setDistance("")
      return;
    }

    const apiRes: any = await sendRequest(formData);
    // setLoading(false);

    if (apiRes && apiRes.status === 200) {

      setFormData({
        source: apiRes.data.src,
        destination: apiRes.data.dest
      })
      setDistance(apiRes.data.distance + " kms.");
    } else {

      setDistance("")
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

  const handleResetForm = () => {
    setFormData({
      source: "",
      destination: ""
    });
    setDistance("");
  }

  return (
    <div>
      <div className="box">
        <label className="label">Source* : </label>
        <input
          type="text"
          name="source"
          value={formData.source}
          placeholder="Enter Start Location"
          onChange={(e) => handleDataChange(e)}
          size={formData.source.length}
        />
      </div>
      <div className="box">
        <label className="label">Destination* : </label>
        <input
          type="text"
          name="destination"
          value={formData.destination}
          placeholder="Enter Destination"
          onChange={(e) => handleDataChange(e)}
          size={formData.destination.length}
        />
      </div>
      <div className="box">
      <label className="label">Geometric Distance : </label>
        <input
          readOnly
          type="text"
          name="destination"
          placeholder="Distance"
          value={distance}
        />
      </div>
      <button className="submit" onClick={handleSubmitForm}>Go!</button>
      <div>
        <button className="reset" onClick={handleResetForm}>Reset</button>
      </div>
    </div>
  );
}

export default CalcDistance;