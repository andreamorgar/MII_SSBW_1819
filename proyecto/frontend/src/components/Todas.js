// components/Todas.js
import React, { Component } from 'react'
import Peli from './Peli'

export default class Todas extends Component {
  constructor(props) {
    super(props)
    this.state = {                // variable estado de la clase, lista de películas
      pelis: []
     }
  }

// llamada al API
componentDidMount() {
  fetch('http://localhost:8000/pelis/tarea12/api_pelis')  // o el que sea
    .then(res => { return res.json()})
    .then(data => {
      console.log(data)
      this.setState({pelis:data})
    }).catch(error => {
      console.log(error)
    })

  }

  render() {
    // re-renderiza al cambiar el state
    return (
      <div>
        <h2><b>Listado de Películas</b></h2> <br />
        {this.state.pelis.map(peli => {  // arrow function
          return (
            <Peli peli={peli} />
          )
        })
      }
      </div>
    )
  }
}
