from django.core.management import setup_environ
import os
import sys
sys.path.append(os.path.dirname(os.path.join('..','wp',__file__)))

import settings
setup_environ(settings)

#==================================#
from arp.models import ConservationFeature as F
from arp.models import Cost
from django.template.defaultfilters import slugify

def output(level,val,crumbs, target=0.0, penalty=0.0):
    id = '---'.join([slugify(x) for x in crumbs])
    print "  "*level, '<span class="specieslabel">', val,'</span>'
    print "  "*level, '''<span class="sliders" id="span---%(id)s">
    <table>
    <tr>
    <td class="treelabel">Goal proportion</td>
    <td><input type="text" class="slidervalue targetvalue" id="target---%(id)s" value="%(target)s"/></td>
    <td><div class="slider" id="slider_target---%(id)s"></div></td>
    </tr>
    <tr>
    <td class="treelabel">Importance weighting</td>
    <td><input type="text" class="slidervalue penaltyvalue" id="penalty---%(id)s" value="%(penalty)s"/></td>
    <td><div class="slider" id="slider_penalty---%(id)s"></div></td>
    </tr>
    </table>
    </span>''' % {'id': id, 'target': target, 'penalty': penalty}

def header():
    print """{% extends "common/panel.html" %}

    {# WARNING: This form is autocreated by the util/generate_fish_list.py script. DO NOT EDIT #}

{% block title %}{{title}}{% endblock %}
{% block panel %}
<script type="text/javascript" charset="utf-8">
    lingcod.onShow(function(){

        var params_impute = function() {
            // If the input json is not null, 
            // Use them to restore the state of the tree
            if ($('#id_input_targets').val() && 
                $('#id_input_penalties').val() && 
                $('#id_input_relativecosts').val()) { 
                 
                //console.log("Restoring Costs slider state...");
                var in_costs = JSON.parse($('#id_input_relativecosts').val());
                $.each(in_costs, function(key, val) {
                    if (val > 0) {
                        $("#cost---" + key).attr('checked','checked')
                    } else {
                        $("#cost---" + key).removeAttr('checked')
                    }
                });

                //console.log("Restoring Targets slider state...");
                var in_targets = JSON.parse($('#id_input_targets').val());
                $.each(in_targets, function(key, val) {
                    $("#target---" + key).val(val);
                });

                //console.log("Restoring Penalties slider state...");
                var in_penalties = JSON.parse($('#id_input_penalties').val());
                $.each(in_penalties, function(key, val) {
                    $("#penalty---" + key).val(val);
                });

                // Restore tree state
                var already_done_clicks = [];
                $.each(in_targets, function(key, val) {
                    //remove the last '---blah' from the key
                    b = key.split('---');
                    b.pop();
                    var id = b.join('---');

                    // If not already done, do a click
                    if (already_done_clicks.indexOf(id) == -1) {
                        $('span#span---' + id).click();
                        already_done_clicks.push(id);
                    }
                });
            };
        }; 

        lingcod.setupForm($('#featureform'));
        $("#focalspecies_tree").treeview({
            collapsed: true
        });

        $('input.slidervalue').click( function(e) {
            // Prevent tree from expanding 
            // when value input field is clicked
            e.stopPropagation();
        });

        params_impute();
       
        var params_collect = function() {
            var targets = {};
            var penalties = {};
            var costs = {};
            var totaltargets = 0;
            var totalpenalties = 0;
            $('.targetvalue:visible').each( function(index) {
                var xid = $(this).attr("id");
                var id = "#" + xid;
                xid = xid.replace(/^target---/,''); //  Remove preceding identifier
                xid = xid.replace(/---$/,''); // Remove trailing ---
                targets[xid] = parseFloat($(id).val());
                totaltargets += parseFloat($(id).val());
            });
            $('.penaltyvalue:visible').each( function(index) {
                var xid = $(this).attr("id");
                var id = "#" + xid;
                xid = xid.replace(/^penalty---/,''); //  Remove preceding identifier
                xid = xid.replace(/---$/,''); // Remove trailing ---
                penalties[xid] = parseFloat($(id).val());
                totalpenalties += parseFloat($(id).val());
            });
            // Initialize costs to zero
            $('input.costvalue[name="cost"]').each( function(index) {
                var xid = $(this).attr("id");
                xid = xid.replace(/^cost---/,''); //  Remove preceding identifier
                costs[xid] = 0;
            });
            // Set the *checked* costs to 1
            $('input.costvalue[name="cost"]:checked').each( function(index) {
                var xid = $(this).attr("id");
                xid = xid.replace(/^cost---/,''); //  Remove preceding identifier
                costs[xid] = 1;
            });
            $('#id_input_targets').val( JSON.stringify(targets) ); 
            $('#id_input_penalties').val( JSON.stringify(penalties) );
            $('#id_input_relativecosts').val( JSON.stringify(costs) );
            if (totalpenalties == 0 || totaltargets == 0) {
                return false;
            } else {
                return true;
            }
        };

        $('.slidervalue').each( function(index) {
            var id = $(this).attr("id");
            var slider_id = "slider_" + id;
            var maxval = 1;
            var minval = 0;
            stepval = 0.01;

            $('#' + slider_id).slider({
                range: 'min',
                min : minval, 
                max : maxval,
                step : stepval,
                change : function(event, ui) {
                    var theval = $(this).slider('value');
                    $('#' + id).val(theval);
                    $('div.slider[id^="' + slider_id + '---"]').each( function() {
                        $(this).slider('value', theval);
                    });
                },
                slide : function(event, ui) {
                    $('#' + id).val($(this).slider('value'));
                }
            });
            $('#' + slider_id).slider('value', $('#' + id).val());
            $('#' + id).change( function(){
                $('#' + slider_id).slider('value', $('#' + id).val());
            });
        });

        // We need to do additional checking so unbind
        $('.submit_button').die('click');
        $('.submit_button').unbind('click');
        // .. and rebind with a validation step
        $('.submit_button').click(function(event){ 
            var proceed = params_collect(); 
            if (proceed) {
                $('#featureform').trigger('submit');
            } else {
                alert("Please specify goals and importance for a least one species of interest. (Step 2)");
            }
        });

        $('#next_1to2').click( function(e) {
            if ($('input#id_name').val() == '') {
                alert("Please provide a name for this watershed prioritization scenario. (Step 1)");
            } else {
                $('#a_step2').click();
            }
        });
        $('#next_2to3').click( function(e) {
            $('#a_step3').click();
        });
        $('#prev_2to1').click( function(e) {
            $('#a_step1').click();
        });
        $('#prev_3to2').click( function(e) {
            $('#a_step2').click();
        });
        $('#a_step1').click( function(e) {
            $('.form_controls').hide();
            $('#controls_step1').show();
        });
        $('#a_step2').click( function(e) {
            $('.form_controls').hide();
            $('#controls_step2').show();
        });
        $('#a_step3').click( function(e) {
            $('.form_controls').hide();
            $('#controls_step3').show();
        });


    });
</script>

<link rel="stylesheet" href="/media/common/js/treeview/jquery.treeview.css" />
<link rel="stylesheet" href="/media/common/js/treeview/jquery-widgets.css" />

    <h1>{{title}}</h1>

            <div class="field required">
                {{ form.input_penalties.errors }}
                {{ form.input_targets.errors }}
                {{ form.input_relativecosts.errors }}
            </div>

<div class="tabs">
    <ul>
        <li>
            <a href="#generaltab" id="a_step1">
                <span>Step 1: Name and <br/> Describe </span>
            </a>
        </li>
        <li>
            <a href="#speciestab" id="a_step2">
                <span>Step 2: Species <br/> of Interest</span>
            </a>
        </li>
        <li>
            <a href="#coststab" id="a_step3">
                <span>Step 3: Prioritization <br/> Constraints</span>
            </a>
        </li>
    </ul>


    <div id="generaltab"> 
    <p>Provide a name and (optionally) a description of the prioritization scenario.</p>
    <form id="featureform" action="{{action}}" method="post"> 
            <div class="hidden field required">
                {{ form.input_penalties.label_tag }}
                {{ form.input_penalties }}            
                {{ form.input_targets.label_tag }}
                {{ form.input_targets }}            
                {{ form.input_relativecosts.label_tag }}
                {{ form.input_relativecosts }}            
                {{ form.input_scalefactor.label_tag}}
                {{ form.input_scalefactor}}
            </div>
            <div class="field required">
                {{ form.name.label_tag }}
                {{ form.name.errors }}
                {{ form.name }}            
            </div>
            <div class="field">
                {{ form.description.label_tag }}
                {{ form.description.errors }}
                {{ form.description }}            
            </div>
            <p><input type="submit" value="submit"></p>
           <div>
           </div>
    </form>
    </div>

    <div id="speciestab">
    <h3>Set Proptions and Weights for Focal Fish Species</h3>
    <p> 
     The <a href="/docs.html#goal" target="_blank">goal proportion</a> is the proportion of the species habitat or viability score you want to represent in your scenario. 
     For example, if a focal species is measured by presence, setting a goal of <em>0.5</em> means that your goal is to conserve at least half of the watersheds containing that species.
     </p>
    <p> 
    The <a href="/docs.html#importance" target="_blank">importance weighting</a> is the subjective value of meeting that goal. 
    Not all goals can always be met due to prioritization constraints - in cases where tradeoffs need to be made, the importance weighting will determine which goals get higher priority. 
    An importance of <em>0</em> means very low priority; <em>1.0</em> means highest priority. 
    </p>
    <br/>
    <form action="#" id="focalspecies_form">
"""

def main():
    """
    Dear lord someone should be shot for writing this
    """
    L1 = F.objects.values_list('level1',flat=True).distinct()
    print "<ul id='focalspecies_tree'>"
    for val1 in L1:
        print "  <li>"
        output(1,val1,[val1])
        L2 = F.objects.filter(level1=val1).values_list('level2',flat=True).distinct().exclude(level2=None).exclude(level2='')
        print "  <ul>"
        for val2 in L2:
            print "    <li>"
            output(2,val2,[val1,val2])
            L3 = F.objects.filter(level1=val1, level2=val2).values_list('level3',flat=True).distinct().exclude(level3=None).exclude(level3='')
            if len(L3) > 0: print "    <ul>"
            for val3 in L3:
                print "      <li>"
                output(3,val3,[val1,val2,val3])
                L4 = F.objects.filter(level1=val1, level2=val2, level3=val3).values_list('level4',flat=True).distinct().exclude(level4=None).exclude(level4='')
                if len(L4) > 0: print "      <ul>"
                for val4 in L4:
                    print "        <li>"
                    output(4,val4,[val1,val2,val3,val4])
                    print "        </li>"
                if len(L4) > 0: print "      </ul>"
                print "      </li>"
            if len(L3) > 0: print "    </ul>"
            print "  </li>"
        if len(L2) > 0: print "  </ul>"
        print "  </li>"
    print "</ul>"

def footer():
    print """ 
    </form></div> <!-- End species tab -->
    <div id="coststab">
        <h3>In addition to focal fish species, prioritize watersheds based the following factors.  </h3>
        <br />
        <form action="#" id="costs_form">
           <div>
            <table>

                <tr>
                <td class="cost"><input type="checkbox" class="costvalue" name="cost" id="cost---watershed-condition" value="watershed-condition" checked="checked"/></td>
                <td><label for="cost---watershed-condition">Watershed Condition</label><p>(favor unimpaired watersheds)</p></td>
                </tr>

                <tr>
                <td class="cost"><input type="checkbox" class="costvalue" name="cost" id="cost---climate" value="climate" checked="checked"/></td>
                <td><label for="cost---climate">Climate Change Vulnerability</label><p>(favor watersheds with low vulnerability to climate change)</p></td>
                </tr>

                <tr>
                <td class="cost"><input type="checkbox" class="costvalue" name="cost" id="cost---invasives" value="invasives" checked="checked"/></td>
                <td><label for="cost---invasives">Vulnerability to Invasive Species</label><p>(favor watersheds with low vulnerability to invasion)</p></td>
                </tr>

    """

    # NOTE: Costs are hardcoded above!
    #for c in Cost.objects.all(): 
    #    cname = slugify(c.name.lower())
    #    print """
    #           <tr>
    #           <td><input type="checkbox" class="costvalue" name="cost" id="cost---%(cname)s" value="%(cname)s" checked="checked"/></td>
    #           <td><label for="cost---%(cname)s">%(full)s</label></td>
    #           </tr>
    #    """ % {'cname': cname, 'full': c.name}

    print """
             </table>
           </div>
        </form>
    </div>
  </div>

    <br class="clear" />
    <div class="form_controls" id="controls_step1">
        <a href="#" class="button" onclick="this.blur(); return false;" id="next_1to2"><span>Next &gt;</span></a>
        <a href="#" class="button" onclick="this.blur(); return false;"><span style="color:#ccc;">&lt; Prev </span></a>
        <a href="#" class="cancel_button button red" onclick="this.blur(); return false;"><span>Cancel</span></a>
        <br class="clear" />
    </div>
    <div class="form_controls" id="controls_step2" style="display:none;">
        <a href="#" class="button" onclick="this.blur(); return false;" id="next_2to3"><span>Next &gt;</span></a>
        <a href="#" class="button" onclick="this.blur(); return false;" id="prev_2to1"><span>&lt; Prev </span></a>
        <a href="#" class="cancel_button button red" onclick="this.blur(); return false;"><span>Cancel</span></a>
        <br class="clear" />
    </div>
    <div class="form_controls" id="controls_step3" style="display:none;">
        <a href="#" class="submit_button button" onclick="this.blur(); return false;"><span>Submit</span></a>
        <a href="#" class="button" onclick="this.blur(); return false;" id="prev_3to2"><span>&lt; Prev </span></a>
        <a href="#" class="cancel_button button red" onclick="this.blur(); return false;"><span>Cancel</span></a>
        <br class="clear" />
    </div>
{% endblock panel %}"""


if __name__ == '__main__':
    header()
    main()
    footer()
