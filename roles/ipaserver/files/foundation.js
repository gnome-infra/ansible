define([
 'freeipa/ipa',
 'freeipa/phases',
 'freeipa/reg',
 'freeipa/field',
 'freeipa/user'],
 function(IPA, phases, reg, field, user_mod) {

// helper function
function get_item(array, attr, value) {
 for (var i=0,l=array.length; i<l; i++) {
 if (array[i][attr] === value) return array[i];
 }

 return null;
}

var foundation_plugin = {};

foundation_plugin.matrix_handle_validator = function(spec) {
 var that = IPA.validator(spec);
 that.message = spec.message || 'Must be in the format localpart:homeserver (e.g. av:gnome.org)';

 that.validate = function(value) {
  if (!value || value === '') return that.true_result();
  var regex = /^[a-zA-Z0-9._=\-\/]+:[a-zA-Z0-9.\-]+$/;
  if (!value.match(regex)) {
   return that.false_result(that.message);
  }
  return that.true_result();
 };

 return that;
};

foundation_plugin.register = function() {
 reg.validator.register('matrix_handle', foundation_plugin.matrix_handle_validator);
};

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

 section.fields.push({
 $type: 'text',
 name: 'matrixhandle',
 label: 'Matrix Handle',
 tooltip: 'Format: localpart:homeserver (e.g. av:gnome.org)',
 validators: [{ $type: 'matrix_handle' }]
 });

 return true;

};

phases.on('registration', foundation_plugin.register);
phases.on('customization', foundation_plugin.add_foundation_fields);
return foundation_plugin;
});
