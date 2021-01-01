
import React, { CSSProperties, useState } from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import InputGroup from 'react-bootstrap/InputGroup';
import FormControl from 'react-bootstrap/FormControl';
import OverlayTrigger from 'react-bootstrap/OverlayTrigger';
import Tooltip from 'react-bootstrap/Tooltip';
import './style.css';

enum COLORSTATUS {
    empty = "empty",
    valid = "valid",
    invalid = "invalid",
    same = "same",
    incomplete = "incomplete"
}

const messageLookup = new Map<COLORSTATUS, string>([
    [COLORSTATUS.empty, "No Color provided"],
    [COLORSTATUS.valid, "Valid Color provided"],
    [COLORSTATUS.invalid, "Color is invalid"],
    [COLORSTATUS.same, "Color is not new"],
    [COLORSTATUS.incomplete, "Color must have 6 characters"]
]);

function ColorInput(props: {
    color: string,
    pages: string,
    updateColors: (color: string, newColor: string | null) => any
}) {

    function copyColorcode(event: React.MouseEvent): void {
        const htmlparagraph_colorcode = event.target as HTMLParagraphElement;
        const temp_input_elem = document.createElement("input");
        temp_input_elem.value = props.color;
        htmlparagraph_colorcode.after(temp_input_elem);
        temp_input_elem.select()
        document.execCommand("copy");
        temp_input_elem.remove();
    }

    const handleOnBlur = () => {
        switch (status) {
            case COLORSTATUS.empty:
            case COLORSTATUS.same:
                props.updateColors(props.color, "");
                break;
            case COLORSTATUS.valid:
                props.updateColors(props.color, value);
                break;
            case COLORSTATUS.invalid:
            case COLORSTATUS.incomplete:
            default:
                props.updateColors(props.color, null);
                break;
        }
    }

    const handleOnChange = (event: React.ChangeEvent) => {
        const nval = (event.target as HTMLInputElement)
            .value
            .replace(/[^a-f0-9]/gi, '')
            .substring(0, 6)
            .toLowerCase();
        switch (nval.length) {
            case 0:
                // input is empty string => reset entry
                // => display default indicator
                setStatus(COLORSTATUS.empty)
                break;
            case 1:
            case 2:
            case 3:
            case 4:
            case 5:
                // color code is invalid as it is less than 6 characters but can still become valid
                // => display soem other indicator
                setStatus(COLORSTATUS.incomplete);
                break;
            case 6:
                if (nval === props.color.replace(/[^a-f0-9]/gi, '')) {
                    // color code is valid but same as original color
                    // => display orange indicator
                    setStatus(COLORSTATUS.same)
                } else {
                    // color code is valid and not same as original color
                    // => display green indicator and color preview
                    setStatus(COLORSTATUS.valid);
                }
                break;
            default:
                // color code is invalid
                // => display red indicator
                // should not be reachable
                setStatus(COLORSTATUS.invalid);
        }
        setValue(nval);
        return;
    }

    const [status, setStatus] = useState(COLORSTATUS.empty);
    const [value, setValue] = useState("");

    return (
        <div>
            <div className="colorcode" style={{ backgroundColor: props.color }}>
                <div
                    id={`pre-${props.color}`}
                    className="right-side"
                    style={{ backgroundColor: `#${value}`, display: status === COLORSTATUS.valid ? "block" : "None" }}
                ></div>
                <p
                    onClick={copyColorcode}>{props.color}
                </p>
            </div>
            <p className="pages">{props.pages}</p>
            <OverlayTrigger
                placement="bottom-start"
                transition={false} // necessary to prevent deprecation warning for findDOMNode
                overlay={
                    <Tooltip
                        id={`tooltip-id-${props.color}`}
                        show={status !== COLORSTATUS.empty}
                    >
                        {messageLookup.get(status)}
                    </Tooltip>}
            >
                {({ ref, ...triggerHandler }) => (
                    <InputGroup
                        {...triggerHandler}>
                        <InputGroup.Prepend>
                            <InputGroup.Text
                                ref={ref}
                                id={`input-${props.color}`}
                                className={status}
                            >#</InputGroup.Text>
                        </InputGroup.Prepend>
                        <FormControl
                            placeholder="new Color"
                            aria-placeholder="new Color"
                            aria-label="new Color"
                            aria-describedby={`input-${props.color}`}
                            value={value}
                            onBlur={handleOnBlur}
                            onChange={handleOnChange}
                        />
                    </InputGroup >
                )}
            </OverlayTrigger>
        </div >
    );
}

export default ColorInput;