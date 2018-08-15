import React from 'react';
import { render } from 'react-dom';
import GeoLocation from './GeoLocation';

const App = () => (
    <GeoLocation />
);

render(<App />, document.getElementById('root'));
