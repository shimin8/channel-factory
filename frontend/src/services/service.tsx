import axios from "axios";

const baseUrl = "http://127.0.0.1:8000/"; // localhost base url added

const FetchLocation = async () => {

    const options = {
        method: 'get',
        url: baseUrl,
        headers: {}
    };
    const apiRes = await axios(options);

    return apiRes.data; // apiRes.data contians the actual json object sent from backend
}

export default FetchLocation;