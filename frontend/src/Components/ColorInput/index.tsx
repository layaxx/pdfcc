
import React, { CSSProperties, useState } from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import InputGroup from 'react-bootstrap/InputGroup';
import FormControl from 'react-bootstrap/FormControl'
import './style.css'

function isValidChar(character: string) {
    return (character >= 'a' && character <= 'f')
        || (character >= 'A' && character <= 'F')
        || (character >= '0' && character <= '9');
}

function isValidColor(color: string): boolean {
    if (color.length === 6) {
        for (let i = 0; i < 6; i++) {
            if (!isValidChar(color.charAt(i))) {
                return false;
            }
        }
        return true;
    } else if (color.length === 7 && color.charAt(0) === '#') {
        for (let i = 1; i < 7; i++) {
            if (color.charAt(i) < 'a' || color.charAt(i) < 'f') {
                return false;
            }
        }
        return true;
    }
    return false;
}


function ColorInput(props: {
    color: string,
    pages: string,
    updateColors: (color: string, newColor: string | null) => any
}) {
    const id_input = "input-" + props.color;
    const id_preview = "pre-" + props.color;

    const [newValue, setNewValue] = useState("");

    // not sure why the as any is needed in the line below, but it doesn´t work without it
    const style_colorcode: CSSProperties = { ["backgroundColor" as any]: props.color };
    return (
        <div>
            <div className="colorcode" style={style_colorcode}>
                <div id={id_preview} className="right-side" style={{ backgroundColor: newValue, display: newValue === "" ? "None" : "block" }}></div>
                <p onClick={(event: React.MouseEvent) => {
                    const htmlparagraph_colorcode = event.target as HTMLParagraphElement;
                    const temp_input_elem = document.createElement("input");
                    temp_input_elem.value = htmlparagraph_colorcode.textContent != null ? htmlparagraph_colorcode.textContent : "";
                    htmlparagraph_colorcode.after(temp_input_elem);
                    temp_input_elem.select()
                    document.execCommand("copy");
                    temp_input_elem.remove();
                }}>{props.color}</p></div>
            <p className="pages">{props.pages}</p>
            <InputGroup>
                <InputGroup.Prepend>
                    <InputGroup.Text id={id_input} >#</InputGroup.Text>
                </InputGroup.Prepend>
                <FormControl
                    placeholder="new Color"
                    aria-placeholder="new Color"
                    aria-label="new Color"
                    aria-describedby={id_input}
                    onBlur={(event: React.FocusEvent) => {
                        const value = (event.target as HTMLInputElement).value;
                        const hashtag_thingy_style = (event.target?.parentNode?.children[0].children[0] as HTMLDivElement).style;
                        if (!(value.length === 0 || value.length === 6 || value.length === 7)) {
                            // Input Element is invalid color => display red, add warning
                            hashtag_thingy_style.backgroundColor = "#dc3545";
                            hashtag_thingy_style.color = "white";
                            props.updateColors(props.color, null);
                            setNewValue("");
                        }
                    }}
                    onChange={(event: React.ChangeEvent) => {
                        const value = (event.target as HTMLInputElement).value;
                        const hashtag_thingy_style = (event.target?.parentNode?.children[0].children[0] as HTMLDivElement).style;
                        if (value.length === 0) {
                            if (value === "") {
                                // Input Element is empty => reset to default
                                hashtag_thingy_style.backgroundColor = "#e9ecef";
                                hashtag_thingy_style.color = "black";
                                props.updateColors(props.color, "");
                                setNewValue("");
                            }
                        } else if (value.length === 6 || value.length === 7) {
                            if (isValidColor(value)) {
                                // Input Element is valid color => display green, add to state
                                hashtag_thingy_style.backgroundColor = "#28a745";
                                hashtag_thingy_style.color = "white";
                                props.updateColors(props.color, value);
                                setNewValue("#" + value);
                            } else {
                                // Input Element is invalid color => display red, add warning
                                hashtag_thingy_style.backgroundColor = "#dc3545";
                                hashtag_thingy_style.color = "white";
                                props.updateColors(props.color, null);
                                setNewValue("");
                            }
                        }
                    }}
                />
            </InputGroup >
        </div >
    );
}

export default ColorInput;