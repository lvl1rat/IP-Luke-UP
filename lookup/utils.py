import requests, random, re, dns.resolver, json
from django.core.cache import cache

CACHE_TIMEOUT = 60 * 15

def sanitize_input(user_input):
    # Remove characters that are not alphanumeric, dots, or dashes
    return re.sub(r'[^A-Za-z0-9.-]', '', user_input)

def switch_query():
    file_path = "iplookup/static/iplookup/json/sw_quotes.json"
    with open(file_path, "r") as file:
        quotes_json = json.load(file)
    quote_entry = random.choice(quotes_json["quotes"])
    return quote_entry["quote"]

def get_ip_data(ip):
    cached_data = cache.get(ip)
    if cached_data:
        return (
            cached_data['data'],
            cached_data['lat_min'],
            cached_data['lat_max'],
            cached_data['lon_min'],
            cached_data['lon_max'],
        )

    try:
        response = requests.get(f'http://ip-api.com/json/{ip}')
        if response.status_code == 200:
            data = response.json()
            if data.get('lat') and data.get('lon'):
                lat_min = round(data['lat'] - 0.025, 15)
                lat_max = round(data['lat'] + 0.025, 15)
                lon_min = round(data['lon'] - 0.05, 15)
                lon_max = round(data['lon'] + 0.05, 15)
                cache.set(
                    ip,
                    {'data': data, 'lat_min': lat_min, 'lat_max': lat_max, 'lon_min': lon_min, 'lon_max': lon_max},
                    timeout=CACHE_TIMEOUT,
                )
                return data, lat_min, lat_max, lon_min, lon_max
            else:
                cache.set(ip, {'data': data}, timeout=CACHE_TIMEOUT)
                return data, None, None, None, None
    except requests.ConnectionError as e:
        return None, None, None, None, None

def generate_map_urls(data, lat_min, lat_max, lon_min, lon_max):
    if data and lat_min and lon_max:
        return {
            'map_url': f"https://www.openstreetmap.org/export/embed.html?bbox={lon_max},{lat_max},{lon_min},{lat_min}&amp;layer=mapnik",
            'shorter_url': f"https://www.openstreetmap.org/#map=14/{data['lat']}/{data['lon']}",
        }
    return {'map_url': None, 'shorter_url': None}

def dns_lookup(domain):
    
    if re.search('[a-zA-Z]', domain):
        dns_record_types = [
            "A",       # Address record: Maps a domain to an IPv4 address.
            "AAAA",    # IPv6 Address record: Maps a domain to an IPv6 address.
            "CNAME",   # Canonical Name record: Alias of one domain to another.
            "MX",      # Mail Exchange record: Directs email to a mail server.
            "TXT",     # Text record: Stores text information, often for verification or other services.
            "NS",      # Name Server record: Delegates a DNS zone to an authoritative server.
            "PTR",     # Pointer record: Maps an IP address to a domain (reverse DNS lookup).
        ]
        for type in dns_record_types:
            try:
                answers = dns.resolver.resolve(domain, type)
                for rdata in answers:
                    print(f"{type} Record: {rdata}")
            except dns.resolver.NoAnswer:
                #print(f"No {type} record found for {domain}")
                continue
            except dns.resolver.NXDOMAIN:
                print(f"Domain {domain} does not exist")
                continue
            except Exception as e:
                print(f"An error occurred: {e}")
                continue