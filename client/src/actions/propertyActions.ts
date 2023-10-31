import axios from "axios";
import { PROPERTY_LISR_REQUEST, PROPERTY_LISR_SUCCESS, PROPERTY_LISR_FAIL } from "./types";


export const listProperties = () => async (dispatch) => {
    try {
        dispatch({
            type: PROPERTY_LISR_REQUEST,
        })
        const {data} = await axios.get("/api/v1/properties/all/")

        dispatch({
            type: PROPERTY_LISR_SUCCESS,
            payload: data
        })
    } catch (error) {
        dispatch({
            type: PROPERTY_LISR_FAIL,
            payload: error.response && error.response.data.message ? error.response.data.message : error.message
        })
    }
}