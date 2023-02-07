import { faCircleXmark } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import React, { useState } from "react";
import { useContext } from "react";
import useFetch from "../../hooks/useFetch";
import "./reserve.css";
import { SearchContext } from "../../context/SearchContext";
// import { Container } from './styles';

const Reserve = ({ setOpen, id }) => {
  const BASE_URL = "http://localhost:8000";
  const { data, loading, error } = useFetch(
    `${BASE_URL}/hotels/hotelroom/${id}`
  );

  const { dates } = useContext(SearchContext);
  const [selectedRooms, setSelectedRooms] = useState([]);
  const handleSelect = (e) => {
    const checked = e.target.checked;
    const value = e.target.value;
    setSelectedRooms(
      checked
        ? [...selectedRooms, value]
        : selectedRooms.filter((item) => item !== value)
    );
  };
  const getDatesInRange = (startDate, endDate) => {
    const start = new Date(startDate);
    const end = new Date(endDate);

    const date = new Date(start.getTime());
    const dates_ = [];
    while (date <= end) {
      dates_.push(new Date(date).getTime());
      date.setDate(date.getDate() + 1);
    }
    return dates_;
  };
  const allDates = getDatesInRange(dates[0].startDate, dates[0].endDate);

  const isAvailable = (roomNumber) => {
    const isFound = roomNumber.unavaliable_dates.some((date) =>
      allDates.includes(new Date(date).getTime())
    );
    return !isFound;
  };
  const handleClick = async () => {
    console.log("Oi");
  };
  return (
    <div className="reserve">
      <div className="rContainer">
        <FontAwesomeIcon
          icon={faCircleXmark}
          className="rClose"
          onClick={() => setOpen(false)}
        />
        <span>Select your rooms:</span>
        {data.map((item) => (
          <div className="rItem" key={item._id}>
            <div className="rItemInfo">
              <div className="rTitle">{item.title}</div>
              <div className="rDesc">{item.desc}</div>
              <div className="rMax">
                Max people: <b>{item.max_people}</b>
              </div>
              <div className="rPrice">{item.price}</div>
            </div>
            <div className="rSelectRooms">
              {item.room_numbers.map((roomNumber) => (
                <div className="room">
                  <label>{roomNumber.number}</label>
                  <input
                    type="checkbox"
                    value={roomNumber._id}
                    onChange={handleSelect}
                    disabled={!isAvailable(roomNumber)}
                  />
                </div>
              ))}
            </div>
          </div>
        ))}
        <button onClick={handleClick} className="rButton">
          Reserve Now!
        </button>
      </div>
    </div>
  );
};

export default Reserve;
