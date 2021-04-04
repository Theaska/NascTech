from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from main.helper import FuncClass

from main.exceptions import FunctionNotFound


class DataSerializer(serializers.Serializer):
    data = serializers.ListField(child=serializers.FloatField())


class MainSerializer(serializers.Serializer):
    """
        Serializer for validating data and rules and applying functions with rules names.
    """
    func_class = FuncClass()
    data = serializers.ListField(child=serializers.FloatField())
    rules = serializers.ListField(child=serializers.CharField())

    def validate_rules(self, rules):
        """
            Validate rules and return list with functions with rules names.
        """
        rules_funcs = []
        for rule in rules:
            try:
                rule_func = self.func_class.get_func(rule)
            except FunctionNotFound as exc:
                raise ValidationError(str(exc))
            rules_funcs.append(rule_func)
            if not rule_func:
                raise ValidationError('Invalid rule name: {}'.format(self.func_class.get_full_func_name(rule)))
        return rules_funcs

    def validate(self, attrs):
        rules = attrs['rules']
        data = attrs['data']
        for rule_func in rules:
            data = list(map(rule_func, data))
        serializer = DataSerializer({'data': data})
        return serializer.data


