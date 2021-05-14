import 'dart:html';
import 'package:flutter/services.dart' show rootBundle;
import 'package:flutter/material.dart';
import 'dart:convert';
import 'dart:async' show Future;
import 'package:flutter/services.dart' show rootBundle;
import 'package:flutter/services.dart';
import 'package:flutter_rating_bar/flutter_rating_bar.dart';

// made by Wybe
Future main() async {
  WidgetsFlutterBinding.ensureInitialized();
  String data = await rootBundle.loadString('assets/data/sorted_wines.json');
  var jsonResult = json.decode(data) as List;
  runApp(MyApp(jsonResult));
}

class MyApp extends StatefulWidget {
  const MyApp(this.data);

  final List data;

  @override
  _MyAppState createState() => _MyAppState();
}

class _MyAppState extends State<MyApp> {
  double price = 30;
  bool ah = true;
  bool gall = true;
  bool jumbo = true;
  bool type_red = true;
  bool type_white = true;
  bool type_rose = true;
  bool type_bubbles = true;
  bool type_other = true;

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'BonusWijn.nl',
      home: Scaffold(
        backgroundColor: Colors.grey[200],
        appBar: AppBar(
          title: Text('Wijn Ladder'),
          backgroundColor: Colors.red[900],
        ),
        drawer: Drawer(
            child: ListView(padding: EdgeInsets.zero, children: [
          Container(
              height: 100,
              child: DrawerHeader(
                  child: Align(
                      alignment: Alignment.center,
                      child: Text("Filters", style: TextStyle(fontSize: 20))))),
          Divider(
            color: Colors.grey[300],
            height: 5,
            thickness: 1,
          ),
          ListTile(
              title: Text("AH"),
              subtitle: Text("Include wines from Albert Heijn"),
              trailing: Switch(
                  activeColor: Colors.red,
                  value: ah,
                  onChanged: (value) {
                    setState(() {
                      ah = value;
                    });
                  })),
          Divider(
            color: Colors.grey[300],
            height: 5,
            thickness: 1,
          ),
          ListTile(
            title: Text("Gall"),
            subtitle: Text("Include wines from Gall&Gall"),
            trailing: Switch(
                activeColor: Colors.red,
                value: gall,
                onChanged: (value) {
                  setState(() {
                    gall = value;
                  });
                }),
          ),
          Divider(
            color: Colors.grey[300],
            height: 5,
            thickness: 1,
          ),
          ListTile(
            title: Text("Jumbo"),
            subtitle: Text("Include wines from Jumbo"),
            trailing: Switch(
                activeColor: Colors.red,
                value: jumbo,
                onChanged: (value) {
                  setState(() {
                    jumbo = value;
                  });
                }),
          ),
          Divider(
            color: Colors.grey[500],
            height: 5,
            thickness: 1,
          ),
          Column(children: [
            Text("Max prijs: " + "€" + price.toString(),
                style: TextStyle(fontWeight: FontWeight.bold)),
            Slider(
              activeColor: Colors.red,
              value: price,
              min: 0,
              max: 30,
              divisions: 30,
              label: "€" + price.round().toString(),
              onChanged: (value) => setState(() => this.price = value),
            ),
          ]),
          Divider(
            color: Colors.grey[500],
            height: 5,
            thickness: 1,
          ),
          SingleChildScrollView(
              child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                CheckboxListTile(
                  title: Text("Rood"),
                  controlAffinity: ListTileControlAffinity.leading,
                  value: type_red,
                  onChanged: (value) {
                    setState(() {
                      type_red = value!;
                    });
                  },
                  activeColor: Colors.red[700],
                  checkColor: Colors.white,
                ),
                Divider(color: Colors.grey.shade400, height: 1.0),
                CheckboxListTile(
                  title: Text("Wit"),
                  controlAffinity: ListTileControlAffinity.leading,
                  value: type_white,
                  onChanged: (value) {
                    setState(() {
                      type_white = value!;
                    });
                  },
                  activeColor: Colors.yellow[100],
                  checkColor: Colors.white,
                ),
                Divider(color: Colors.grey.shade400, height: 1.0),
                CheckboxListTile(
                  title: Text("Rose"),
                  controlAffinity: ListTileControlAffinity.leading,
                  value: type_rose,
                  onChanged: (value) {
                    setState(() {
                      type_rose = value!;
                    });
                  },
                  activeColor: Colors.red[100],
                  checkColor: Colors.white,
                ),
                Divider(color: Colors.grey.shade400, height: 1.0),
                CheckboxListTile(
                  title: Text("Bubbles"),
                  controlAffinity: ListTileControlAffinity.leading,
                  value: type_bubbles,
                  onChanged: (value) {
                    setState(() {
                      type_bubbles = value!;
                    });
                  },
                  activeColor: Colors.yellow[50],
                  checkColor: Colors.white,
                ),
                Divider(color: Colors.grey.shade400, height: 1.0),
                CheckboxListTile(
                  title: Text("Other"),
                  controlAffinity: ListTileControlAffinity.leading,
                  value: type_other,
                  onChanged: (value) {
                    setState(() {
                      type_other = value!;
                    });
                  },
                  activeColor: Colors.grey[400],
                  checkColor: Colors.white,
                ),
                Divider(color: Colors.grey.shade500, height: 1.0),
              ])),
        ])),

        // Body of the webapp
        body: Center(
          child: WineList(
              widget.data,
              this.price,
              this.ah,
              this.gall,
              this.jumbo,
              this.type_red,
              this.type_white,
              this.type_rose,
              this.type_bubbles,
              this.type_other),
        ),
      ),
    );
  }
}

class WineList extends StatelessWidget {
  const WineList(
      this.wine_data,
      this.price,
      this.ah,
      this.gall,
      this.jumbo,
      this.type_red,
      this.type_white,
      this.type_rose,
      this.type_bubbles,
      this.type_other);

  final List wine_data;
  final double price;
  final bool ah;
  final bool gall;
  final bool jumbo;
  final bool type_red;
  final bool type_white;
  final bool type_rose;
  final bool type_bubbles;
  final bool type_other;

  @override
  Widget build(BuildContext context) {
    return ListView.builder(
      padding: const EdgeInsets.all(2),
      itemCount: wine_data.length,
      itemBuilder: (BuildContext context, int index) {
        final item = wine_data[index];
        final store = item['store'];
        final type = item['type'];

        if (item['bonusPrice'] <= price &&
            ((ah && store == 'AH') ||
                (gall && store == "GALL") ||
                (jumbo && store == 'Jumbo')) &&
            ((type_red && type == 'Red') ||
                (type_rose && type == 'Ros\u00e9') ||
                (type_white && type == 'White') ||
                (type_bubbles && type == 'Bubbles'))) {
          return Container(
            height: 100,
            child: Center(
                child: Wine(
                    wine_data[index]['title'],
                    wine_data[index]['originalPrice'],
                    wine_data[index]['bonusPrice'],
                    wine_data[index]['rating'],
                    wine_data[index]['numberOfReviews'],
                    wine_data[index]['store'],
                    item['type'])),
          );
        } else {
          return Container(height: 0.0001);
        }
      },
      // separatorBuilder: (BuildContext context, int index) => const Divider(),
    );
  }
}

// Tiles
class Wine extends StatelessWidget {
  const Wine(this.name, this.original_price, this.bonus_price, this.rating,
      this.reviews, this.store, this.type);

  final String name;
  final double original_price;
  final double bonus_price;
  final double rating;
  final int reviews;
  final String store;
  final String type;

  @override
  Widget build(BuildContext context) {
    return Padding(
        padding: const EdgeInsets.symmetric(vertical: 1.0, horizontal: 4.0),
        child: Card(
            child: Padding(
                padding: EdgeInsets.all(10),
                child: Row(children: [
                  Image.asset(
                      'assets/images/' + name.replaceAll(" ", "") + ".PNG"),
                  Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                        this.name,
                        style: TextStyle(fontSize: 15),
                        overflow: TextOverflow.ellipsis,
                      ),
                      Row(children: [
                        Column(
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: [
                              Row(children: [
                                Text(
                                  "€" + this.bonus_price.toString() + " ",
                                  style: TextStyle(
                                      fontWeight: FontWeight.bold,
                                      color: Colors.deepOrange.withOpacity(1)),
                                ),
                                Text(
                                  " €" + this.original_price.toString(),
                                  style: TextStyle(
                                      fontSize: 10,
                                      decoration: TextDecoration.lineThrough),
                                ),
                                Text("  0,75 l",
                                    style: TextStyle(
                                        fontSize: 10, color: Colors.grey[400]))
                              ]),
                              Text("Store: " + this.store,
                                  style: TextStyle(
                                    fontSize: 12,
                                  )),
                            ]),
                        Column(children: [
                          Text(this.rating.toString(),
                              style: TextStyle(
                                  fontSize: 15, fontWeight: FontWeight.bold)),
                          RatingBarIndicator(
                            rating: this.rating,
                            itemBuilder: (context, index) => Icon(
                              Icons.brightness_1_rounded,
                              color: Colors.red[700],
                            ),
                            itemCount: 5,
                            itemSize: 10.0,
                            direction: Axis.horizontal,
                          ),
                          Text(this.reviews.toString() + " reviews",
                              style: TextStyle(
                                fontSize: 12,
                              )),
                        ]),
                      ])
                    ],
                  )
                ]))));
  }
}
