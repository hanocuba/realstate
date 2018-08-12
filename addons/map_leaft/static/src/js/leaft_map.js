odoo.define('map_leaft.FieldMap', function(require) {
    "use strict";

    var core = require('web.core');
    var Model = require('web.DataModel');
    var form_common = require('web.form_common');

    var FieldMap = form_common.AbstractField.extend({
        template: 'map_template',

        start: function() {
            var self = this;

            var id = self.get("value")[0]

            var mymap = L.map(self.$el[0]).setView([21.363, -79.407], 7);

            self.refresh_map(id, mymap, self);

            mymap.on('click', function (e) {

                if(!self.get("effective_readonly")) {
                    self.do_action({
                        type: 'ir.actions.act_window',
                        res_model: 'map_leaft.marker',
                        target: 'new',
                        res_id: '',
                        views: [[false, 'form']],
                        context: {'default_map_id': id, 'default_lat': e.latlng.lat, 'default_lon': e.latlng.lng}
                    }, {
                        on_close: function (result) {
                            self.refresh_map(id, mymap, self)
                        }
                    })
                }

            });

            L.tileLayer('http://localhost:8089/styles/osm-bright/?raster#{z}/{x}/{y}', {
                attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
                maxZoom: 18
            }).addTo(mymap);

            // var circle = L.circle([51.508, -0.11], {
            //     color: 'red',
            //     fillColor: '#f03',
            //     fillOpacity: 0.5,
            //     radius: 500
            // }).addTo(mymap);

            self.myMap = mymap

            this.update_mode();
            this._super();
        },
        refresh_map: function (id, mymap, self) {
            new Model("map_leaft.marker")
                .query(["id", "name", "lat", "lon"])
                .filter([['map_id', '=', id]])
                .all()
                .then(function(result) {
                    _(result).each(function (item) {
                        var marker = L.marker([item.lat, item.lon],
                            {iconUrl: 'marker-icon.png', iconRetinaUrl: 'marker-icon.png'}).addTo(mymap);
                        marker.object_id = item.id

                        var divParent = document.createElement("div");
                        divParent.innerHTML = "<b>Panadería</b><br/><bold>" + item.name + "</bold>"

                        divParent.appendChild(document.createElement("br"))

                        var a = document.createElement("a");
                        a.innerHTML = "Info"
                        a.onclick = function () {

                            self.do_action({
                                type: 'ir.actions.act_window',
                                res_model: 'map_leaft.marker',
                                target: 'new',
                                res_id: item.id,
                                views: [[false, 'form']]
                            }, {
                                on_close: function(event){
                                    self.refresh_map(id, mymap, self)
                                    // location.reload()
                                }
                            })
                        };

                        divParent.appendChild(a)

                        marker.bindPopup(divParent)
                    });
                });
        },
        render_value: function() {

        },
        update_mode: function() {
            if(this.get("effective_readonly")) {

            } else {

            }
        },
        _toggle_label: function() {
            this._super();
            // google.maps.event.trigger(this.map, 'resize');
            if (!this.no_rerender) {
                this.render_value();
            }
        },
    });

    core.form_widget_registry.add('leaft_map', FieldMap);

    var GalleriaWdg = form_common.AbstractField.extend({
        template: 'map_galleria',

        start: function() {
            this._super();
            // this.on("change:mode", this, function () {
            //     console.log("MODE CHANGTEDdddddddd")
            // });
            console.log("STARTING")

            // this.update_mode();
            //
            //
            // this.galleria_render();
        },
        set_value: function(value_) {
            var self = this;
            console.log('SETTING THE VALUE--- ' + $(self.$el).is(':visible'))
            console.log(value_)

            if(value_)
            {
                var candidates = value_.split(",")
                console.log("CANDIDATEES")
                console.log(candidates)
                var values = []
                for(var i = 0; i < candidates.length; ++i)
                {
                    var current = candidates[i]
                    if(!isNaN(current))
                    {
                        values.push(parseInt(current))
                    }
                }

                self.set({'value': values});
            }

            this._super(values)

            //     .then(function () {
            //     if (self.is_started && !self.no_rerender) {
            //         return self.reload_current_view();
            //     }
            //     else{
            //         self.galleria_render()
            //     }
            // });


            // self._super(value_).then(function () {
            //
            //     if (self.is_started && !self.no_rerender) {
            //         // return self.reload_current_view();
            //     }
            // });

        },
        get_value: function () {
            return this.get("value")
        },
        refresh_map: function (id, mymap, self) {
            console.log("refresh map")
        },
        render_value: function() {
            var self = this;

            var value = self.get("value")
            if(value)
            {
                console.log("Rendering")

                console.log("Requesting " + value)

                // self.galleria_render()

                // myNode.remove()
                $(self.$el).children().remove()
                if($(self.$el).children().length > 0)
                {
                    console.log("DESTROY GALLERIA")
                    if(Galleria.get(0) !== undefined)
                    {
                        Galleria.get(0).destroy()
                    }
                }

                console.log(self.options.gallery_model)

                new Model(self.options.gallery_model)
                    .query(["id", "name", "image", "description"])
                    .filter([['id', 'in', value]])
                    .all()
                    .then(function(result) {
                        var img_list = new Array()
                        var $myNode = $(self.$el)

                        console.log("----------*************************")
                        console.log($myNode)
                        // $myNode.children().remove()

                        console.log("----------*************************")
                        var first_time = ($(self.$el).children().length == 0)
                        _(result).each(function (item) {
                            if(first_time)
                            {
                                var img = $("<img/>").attr("src", "data:image/png;base64," + item.image).attr("data-description", "<i>Descripción</i><br/>" + item.description)
                                $myNode.append(img)
                            }
                            else
                            {
                                img_list.push({src_id: item.id,image: "data:image/png;base64," + item.image})
                            }
                            console.log("appending")
                        })

                        console.log()

                        // console.log(img_list)
                        // var g2 = Galleria.get(0)
                        // console.log(Galleria.get(0))
                        // Galleria.get(0).splice( 0, 2 );
                        // Galleria.get(0).load(img_list)
                        // console.log($(self.$el))

                        if(first_time)
                        {
                            Galleria.loadTheme('/map_leaft/static/src/js/galleria.classic.min.js');
                            Galleria.run($(self.$el), {wait: true, lightbox: true, idleMode: true, fullscreenCrop: true});
                        }
                        else
                        {
                            if(Galleria.get(0) !== undefined)
                            {
                                Galleria.get(0).load(img_list)
                            }
                        }


                        // var $galleria = $(self.$el).data('galleria')
                        // $galleria.load(img_list)

                        // console.log(g === g2)
                    });

                // $(myNode).find("div").remove()

                // self.galleria_render()
            }
        },
        update_mode: function() {

            console.log("Update Model")
            if(this.get("effective_readonly")) {

            } else {

            }

        },
        _toggle_label: function() {
            console.log("TOOGLE LABEL")
            this._super();
            // google.maps.event.trigger(this.map, 'resize');
            if (!this.no_rerender) {

            }
        },
    });

    core.form_widget_registry.add('leaft_gallery', GalleriaWdg);

    return {
        FieldMap: FieldMap,
    };

});