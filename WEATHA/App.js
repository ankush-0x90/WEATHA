/**
 * Sample React Native App
  https://github.com/asprazz
 * @flow
 */
import React, { Component } from 'react';
import {
  
  Platform,
  StyleSheet,
  Text,
  View,
  Image,
  ImageBackground,
  WebView
} from 'react-native';

export default class App extends Component<> {
  render() {
    
    const resizeMode = 'center';
    const text = 'This is some text inlaid in an <Image />';

    return (
      /*from sujit's web*/
      <WebView
             source={{uri: 'http://192.168.42.201:5000'}}
             style={{marginTop: 0}}
      />

    );
  }
}

const styles = StyleSheet.create({
  wrapper: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#fff',
  },
  welcomeText: {
    color:'#c0392b',
    fontSize:35,
    fontWeight:'bold'
  }
});

