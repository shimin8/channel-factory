import { useEffect, useState } from "react";
import FetchLocation from "./services/service";

const App = () => {
  const [message, setMessage] = useState("");

  useEffect( () => {

    const func = async () => {
      const resp = await FetchLocation();
      console.log(resp);
      setMessage(resp.msg);
    };

    func();
  }, []);

  return (
    <div>
      <h1>{message || "Loading..."}</h1>
    </div>
  )
}

export default App;