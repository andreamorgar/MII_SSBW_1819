// components/Peli.js
import React, { Component } from 'react'

export default class Peli extends Component {

	render() {

	var peli = this.props.peli  // props desde el componente de arriba
	return(
	   <div key={peli.id}>
	      <h6>{peli.title}</h6>

	      <hr />
	   </div>
   );
	}
}
