import { PROPERTY_LISR_FAIL, PROPERTY_LISR_REQUEST, PROPERTY_LISR_SUCCESS } from "../actions/types";


export const propertiesListReducer = (state = {properties: []}, action) => {
    switch (action.type) {
        case PROPERTY_LISR_REQUEST:
            return {loading: true, properties:[]}

        case PROPERTY_LISR_SUCCESS:
            return {loading: false, properties:action.payload.results}

        case PROPERTY_LISR_FAIL:
            return {loading: false, error: action.payload}
            
        default:
            return state;
    }
}