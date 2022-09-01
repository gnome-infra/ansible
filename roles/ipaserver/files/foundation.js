define([
 'freeipa/phases',
 'freeipa/user'],
 function(phases, user_mod) {

// helper function
function get_item(array, attr, value) {
 for (var i=0,l=array.length; i<l; i++) {
 if (array[i][attr] === value) return array[i];
 }

 return null;
}

var foundation_plugin = {};

foundation_plugin.add_foundation_fields = function() {

 var facet = get_item(user_mod.entity_spec.facets, '$type', 'details');
 var section = get_item(facet.sections, 'name', 'identity');
 section.fields.push({
 name: 'firstadded',
 label: 'Foundation Member since'
 });

 section.fields.push({
 name: 'lastrenewedon',
 label: 'Last Renewed on date'
 });

 section.fields.push({
 name: 'description',
 label: 'Previous account changes'
 });

 return true;

};

phases.on('customization', foundation_plugin.add_foundation_fields);
return foundation_plugin;
});
