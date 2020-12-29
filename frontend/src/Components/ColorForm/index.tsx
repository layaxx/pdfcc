import React, { useState } from 'react';
import ColorInput from '../ColorInput'
import './style.css';
import 'animate.css';
import Button from 'react-bootstrap/Button';
import Spinner from 'react-bootstrap/Spinner';
import update from 'immutability-helper';
import Alert from 'react-bootstrap/Alert';

// TODO: exclude pages

function ColorForm(props: { state: () => any, handleChange: (b64: string) => any }) {
    const state = props.state();
    const colors = state.colors;
    const file = state.file;

    const [formState, setFormState] = useState({
        mapOldColorsToNewColors: new Map(),
        errors: new Set(),
        alert: {
            type: "danger",
            msg: "You submitted invalid new colors for: ",
            active: false
        },
        waitingForServerResponse: false
    });

    const colorInputsArray: Array<JSX.Element> = [];

    for (var index in colors) {
        colorInputsArray.push(
            <ColorInput
                updateColors={(color: string, newColor: string | null) => {
                    if (newColor === null) {
                        // Error-Case
                        setFormState((state) => update(state, {
                            mapOldColorsToNewColors: { $remove: [color] },
                            errors: { $add: [color] }
                        }));
                    } else if (newColor === "") {
                        // Reset-Case
                        setFormState((state) => update(state, {
                            mapOldColorsToNewColors: { $remove: [color] },
                            errors: { $remove: [color] }
                        }));
                    } else {
                        // Valid-Color-Case
                        setFormState((state) => update(state, {
                            mapOldColorsToNewColors: { $add: [[color, newColor]] },
                            errors: { $remove: [color] }
                        }));
                    }
                }}
                key={index}
                color={colors[index][0]}
                pages={colors[index][1]}
            />);
    }

    return (
        <form id="form-colors" autoComplete="off">
            <p><b>Showing Colors for: </b>{file.name}</p>
            <div className="analysis_result">
                {colorInputsArray}
            </div>
            <div className="status-wrapper">
                <Alert
                    variant={formState.alert.type}
                    id="submit-status"
                    hidden={formState.errors.size === 0 && !formState.alert.active}>
                    <Spinner
                        animation="border"
                        role="status"
                        hidden={formState.alert.msg !== "Waiting for Server response..."}></Spinner>
                    {formState.alert.msg + (formState.errors.size !== 0 ? Array.from(formState.errors).join(", ") : "")}
                </Alert>
            </div>
            <Button type="submit"
                onClick={
                    ((event: React.MouseEvent) => {
                        event.preventDefault();
                        if (formState.errors.size !== 0) {
                            const element = document.querySelector('#submit-status');
                            element?.classList.add('animate__animated', 'animate__pulse');
                            setTimeout(function () {
                                element?.classList.remove('animate__pulse');
                            }, 1000);
                        } else if (formState.mapOldColorsToNewColors.size > 0) {
                            setFormState((state) => update(state, {
                                alert: {
                                    active: { $set: true },
                                    type: { $set: "info" },
                                    msg: { $set: "Waiting for Server response..." }
                                }
                            }));
                            var data: FormData = new FormData();
                            const pdf = file as Blob;
                            data.append('file', pdf);
                            formState.mapOldColorsToNewColors.forEach((value, key) => {
                                data.append(key, value);
                            });
                            fetch("/ajax/process", {
                                method: 'POST',
                                body: data
                            })
                                .then(response => {
                                    if (!response.ok) {
                                        throw Error(response.statusText);
                                    }
                                    return response;
                                })
                                .then(response => response.json())
                                .then(response => {
                                    if (response.error) {
                                        setFormState((state) => update(state, {
                                            alert: {
                                                active: { $set: true },
                                                type: { $set: "danger" },
                                                msg: { $set: "Request came back with the following error message: " + response.message }
                                            }
                                        }));
                                    } else {
                                        props.handleChange(response.b64);
                                    }
                                })
                                .catch(function (error) {
                                    setFormState((state) => update(state, {
                                        alert: {
                                            active: { $set: true },
                                            type: { $set: "danger" },
                                            msg: { $set: "Request failed: " + error }
                                        }
                                    }));
                                });
                        }
                    })
                }
                block
                disabled={formState.alert.msg === "Waiting for Server response..."}>
                {formState.alert.msg !== "Waiting for Server response..." ? "Submit Colors" : "Waiting..."}</Button>
        </form >

    );
}

export default ColorForm;

