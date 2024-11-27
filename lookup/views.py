from django.shortcuts import render
from django.http import HttpResponse
from .utils import get_ip_data, switch_query, generate_map_urls, dns_lookup
import re, socket

from django.template import engines

CACHE_TIMEOUT = 60 * 15

def vuln_user_input_handler(request):
    message = request.GET.get('message')
    quote = switch_query()
    return render(request, 'index.html', {'quote': quote, 'message': message})


def ip_lookup(request):
    valid_ip_regex = r'\b((25[0-5]|2[0-4]\d|1\d{2}|[1-9]?\d)\.){3}(25[0-5]|2[0-4]\d|[1-9]?\d)\b'
    valid_dns_regex = r'/^(?!:\/\/)([a-zA-Z0-9-_]+\.)*[a-zA-Z0-9][a-zA-Z0-9-_]+\.[a-zA-Z]{2,11}?$/'
    valid_ipv6_regex = r'/^(([0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,7}:|([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2}|([0-9a-fA-F]{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3}|([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}|([0-9a-fA-F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6})|:((:[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(:[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(ffff(:0{1,4}){0,1}:){0,1}((25[0-5]|2[0-4][0-9]|[0-1]?[0-9]{1,2})\.){3,3}(25[0-5]|2[0-4][0-9]|[0-1]?[0-9]{1,2})|([0-9a-fA-F]{1,4}:){1,4}:((25[0-5]|2[0-4][0-9]|[0-1]?[0-9]{1,2})\.){3,3}(25[0-5]|2[0-4][0-9]|[0-1]?[0-9]{1'

    # Check if the request contains an IP or DNS query
    ip = request.GET.get('ip', None)
    dns = request.GET.get('dns', None)
    message = request.GET.get('message', None)
    
    if message:
        quote = switch_query()
        engine = engines["django"]
        template = engine.from_string("<div>"+message+"</div>")
        return HttpResponse(template.render({}, request))

    if ip:
        # Validate the IP address
        if not re.fullmatch(valid_ip_regex, ip):
            quote = switch_query()
            return render(request, 'index.html', {'quote': 'Invalid IP address', 'error': 'Invalid IP address'})

        # Process the IP address
        data, lat_min, lat_max, lon_min, lon_max = get_ip_data(ip)
        map_urls = generate_map_urls(data, lat_min, lat_max, lon_min, lon_max)
    elif dns:
        if not re.fullmatch(valid_dns_regex, dns):
            quote = switch_query()
            return render(request, 'index.html', {'quote': 'Invalid DNS address', 'error': 'Invalid DNS address'})
        # Resolve the DNS query to an IP address
        try:
            resolved_ip = socket.gethostbyname(dns)
            dns_lookup(dns)
            data, lat_min, lat_max, lon_min, lon_max = get_ip_data(resolved_ip)
            map_urls = generate_map_urls(data, lat_min, lat_max, lon_min, lon_max)
        except socket.gaierror:
            quote = switch_query()
            return render(request, 'index.html', {'quote': quote, 'error': 'Invalid domain name'})
    else:
        # No valid input provided
        quote = switch_query()
        return render(request, 'index.html', {'quote': quote, 'error': 'Please enter an IP or domain'})

    # Render the response for a valid lookup
    test = "test"
    quote = switch_query()
    response = render(request, 'index.html', {
        'ip_data': data,
        'searched_ip': ip or dns,
        **map_urls,
        'quote': quote,
        
    })
    response['ngrok-skip-browser-warning'] = 'true'

    return response


def about(request):
    return render(request, 'about.html')


def contact(request):
    return render(request, 'contact.html')
