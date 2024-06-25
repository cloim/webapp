import { custom_event, get_current_component } from 'svelte/internal';
import { format, add } from "date-fns";

export const d = (...args) => {
    for (const arg of args) {
        if (isObj(arg)) {
            console.log(JSON.stringify(arg, null, 2));
        } else {
            console.log(`${arg}\n`);
        }
    }
}

export const createEventDispatcher = () => {
    const component = get_current_component();

    return (type, detail) => {
        const callbacks = component.$$.callbacks[type];

        if (callbacks) {
            const arr = [];
            const hasCallbacks = !!callbacks.length;
            const event = custom_event(type, detail);
            callbacks.slice().forEach(fn => {
                const res = fn.call(component, event);
                if (res instanceof Promise) {
                    arr.push(res);
                }
            });
            return Promise.all(arr).then(() => hasCallbacks);
        }
        return new Promise((resolve) => resolve(false));
    };
}

export const isObj = (val) => {
    if (val === null) {
        return false;
    }

    return ((typeof val === 'function') || (typeof val === 'object'));
}

export const typeOf = (val) => {
    try {
        if (typeof val === "object") return "json";
        var json = JSON.parse(val);
        if (typeof json === "object") return "jsonstr";
    } catch (e) {
        return typeof val;
    }
}

export const findIndexByKeyValue = (jsonArray, key, value) => {
    for (let i = 0; i < jsonArray.length; i++) {
        if (jsonArray[i][key] === value) {
            return i;
        }
    }
    return -1;
}

export const addNewObjectAtIndex = (jsonArray, index, newObj) => {
    index = Math.min(index, jsonArray.length);
    jsonArray.splice(index, 0, newObj);
}

export const dateFormat = (date, dateOnly) => {
    const year = date.getFullYear();
    const month = date.getMonth() + 1;
    const month_str = month < 10 ? `0${month}` : `${month}`;
    const day = date.getDate();
    const day_str = day < 10 ? `0${day}` : `${day}`;
    const hour = date.getHours();
    const minute = date.getMinutes();
    const second = date.getSeconds();

    if (dateOnly) {
        return `${year}-${month_str}-${day_str}`;
    }
    return `${year}-${month_str}-${day_str} ${hour}:${minute}:${second}`;
}

export const createTimeArray = (time_s, time_e, m_step) => {
    let current = new Date(`2024-01-01T${time_s.substring(0, 2)}:${time_s.substring(time_s.length - 2)}:00`);
    const end = new Date(`2024-01-01T${time_e.substring(0, 2)}:${time_e.substring(time_e.length - 2)}:00`);
    let timeArray = [];

    while (current <= end) {
        timeArray.push({ name: format(current, "HH:mm"), value: format(current, "HHmm") });
        current = add(current, { minutes: m_step });
    }

    return timeArray;
}

export const createNumbersForSelect = (s_no, e_no, step) => {
    const result = [];
    
    for (let i = s_no; i <= e_no; i += step) {
        result.push({ name: i, value: i });
    }

    return result;
}

export const formatCellPhoneNo = (cell_phone_no) => {
    if (cell_phone_no.includes('-')) {
        return cell_phone_no;
    }
    
    const digits = cell_phone_no.replace(/\D/g, '');
    if (digits.length !== 11) {
        throw new Error('Invalid phone number length. It should be 10 digits.');
    }
    
    return `${digits.slice(0, 3)}-${digits.slice(3, 7)}-${digits.slice(7)}`;
}

export const getTypeInfo = (apiTypes, api) => {
    if (!api.type) return null;

    const typeInfo = apiTypes.find(t => t.type_id === api.type);
    if (!typeInfo) return null;

    return {
        typeType: typeInfo.type_type,
        langID: typeInfo.lang_id,
        tabSize: typeInfo.tab_size,
        iconID: typeInfo.icon_id,
        iconColor: typeInfo.icon_color || ""
    }
}

export const setTypeInfo = (apiTypes, apis) => {
    const newAPIs = [];

    for (const api of apis) {
        if (Object.hasOwn(api, "children")) {
            const newAPI = {
                id: api.id,
                name: api.name
            }
            const childrens = setTypeInfo(apiTypes, api.children);
            newAPI.children = childrens;
            newAPIs.push(newAPI);
        } else {
            const typeInfo = getTypeInfo(apiTypes, api);
            Object.assign(api, typeInfo);
            newAPIs.push(api);
        }
    }
    return newAPIs;
}

export const copyToClipboard = async (text) => {
    try {
        await navigator.clipboard.writeText(text);
        return true;
    } catch (err) {
        return false;
    }
}