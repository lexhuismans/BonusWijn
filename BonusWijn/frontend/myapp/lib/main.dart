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

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'BonusWijn.nl',
      home: Scaffold(
        backgroundColor: Colors.grey[200],
        appBar: AppBar(
          title: Text('De Beste Deals'),
          backgroundColor: Colors.red,
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
        ])),
        body: Center(
          child: WineList(widget.data, this.price, this.ah, this.gall),
        ),
      ),
    );
  }
}

class WineList extends StatelessWidget {
  const WineList(this.wine_data, this.price, this.ah, this.gall);

  final List wine_data;
  final double price;
  final bool ah;
  final bool gall;

  @override
  Widget build(BuildContext context) {
    return ListView.builder(
      padding: const EdgeInsets.all(2),
      itemCount: wine_data.length,
      itemBuilder: (BuildContext context, int index) {
        final item = wine_data[index];
        final store = item['store'];

        if (item['bonusPrice'] <= price &&
            ((ah && store == 'AH') || (gall && store == "GALL"))) {
          return Container(
            height: 100,
            child: Center(
                child: Wine(
                    wine_data[index]['title'],
                    wine_data[index]['originalPrice'],
                    wine_data[index]['bonusPrice'],
                    wine_data[index]['rating'],
                    wine_data[index]['numberOfReviews'],
                    wine_data[index]['store'])),
          );
        } else {
          return Container(height: 0.0001);
        }
      },
      // separatorBuilder: (BuildContext context, int index) => const Divider(),
    );
  }
}

class Wine extends StatelessWidget {
  const Wine(this.name, this.original_price, this.bonus_price, this.rating,
      this.reviews, this.store);

  final String name;
  final double original_price;
  final double bonus_price;
  final double rating;
  final int reviews;
  final String store;

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
                              Icons.star,
                              color: Colors.amber,
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
