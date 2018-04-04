// @flow

import React, {Component} from 'react';
import {AppRegistry, ScrollView, Text, View} from 'react-native';

import {
  DrawerItems,
  DrawerNavigator,
  StackNavigator,
  TabNavigator
} from 'react-navigation';


import {HomeScreen} from '../HomeScreen';
import {DetailsScreen1} from '../DetailsScreen1';
import {DetailsScreen2} from '../DetailsScreen2';
import {SettingsScreen} from '../SettingsScreen';

import * as css from '../Styles';
import {Icon} from 'react-native-elements';

import {Provider} from 'react-redux';
import {store} from '../state/Context';


const NavTab = TabNavigator(
  // route config
  {
    DetailsRoute1: {screen: DetailsScreen1},
    DetailsRoute2: {screen: DetailsScreen2},
  },
  // navigator config
  {
    lazyLoad      : false, // render the tabs lazily
    tabBarPosition: 'bottom', // where are the tabs shown
    backBehavior  : 'none', // back button doesn't take you to the initial tab
    tabBarOptions : css.tabs,
  },
);

//
// STACK
//

const titleAndIcon =
        <View style={css.header.container}>
          <Icon name="wb-sunny" color={css.colors.text_light}/>
          <Text style={css.header.text}>WEATHA</Text>
        </View>;

const NavStack = StackNavigator(
  // route config
  {
    HomeRoute   : {screen: HomeScreen}, // this is displayed first
    DetailsRoute: {screen: NavTab},
  },
  // navigator config
  {
    //headerMode: 'none', // this removes the navigation header
    navigationOptions: {
      // labe l text
      headerTitle: titleAndIcon,
      // other styling
      ...css.header,
    },
  },
);

const customDrawerComponent = (props) =>
  
  <ScrollView
    style={{
      flex           : 1,
      backgroundColor: css.drawer.style.backgroundColor,
    }}>
    <DrawerItems {...props} />
  </ScrollView>;

const NavDrawer = DrawerNavigator(
  // route config
  {
    HomeRoute    : {
      screen           : NavStack,
      navigationOptions: {
        drawerLabel: 'Weatha',
        drawerIcon : ({tintColor}) => <Icon name="wb-sunny" color={tintColor}/>,
      },
    },
    SettingsRoute: {
      screen           : SettingsScreen,
      navigationOptions: {
        drawerLabel: 'About Team',
        drawerIcon : ({tintColor}) => <Icon name="settings" color={tintColor}/>,
      },
    },
  },
  // navigator config
  {
    contentComponent: customDrawerComponent,
    drawerPosition  : 'left',
    // styling for for DrawerView.Items in contentOptions
    contentOptions  : css.drawer,
  },
);

class Root extends Component {
  render() {
    return (
      <Provider store={store}>
        <NavDrawer/>
      </Provider>
    );
  }
}

AppRegistry.registerComponent('WeatherApp', () => Root);