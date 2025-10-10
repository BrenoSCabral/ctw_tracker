from scipy import signal


def low_pass(xdays):
    dt = xdays
    pesos = 10
    periodo_min = 3
    cutoff_max = 1 / periodo_min
    fn = 1/(2*dt)

    b, a = signal.butter(pesos, cutoff_max/fn,
                        btype='low')

    return (b,a)


def high_pass():
    '''
    Nesse caso, precisa rodar para o ssh já reamostrado em 1 dia
    '''
    dt = 1
    periodo = 30
    cutoff = 1 / periodo
    fn = 1/(2*dt)

    b, a = signal.butter(14, cutoff/fn,
                        btype='high')

    return (b,a)


def apply_filter(b,a, nivel_mar):
    nivel_mar_filtrado = signal.filtfilt(b, a, nivel_mar)

    return nivel_mar_filtrado


def filter_data(data):

    b, a = low_pass(1/24)
    ssh = list(data['ssh'])
    ssh_low_pass = apply_filter(b,a, ssh)
    
    data['low_pass'] = ssh_low_pass
    daily_data = data[data.index.hour == data.index.hour[-1]]
    ssh_low_pass_daily = list(daily_data['low_pass'])

    b, a = high_pass()
    ssh_filt = apply_filter(b,a, ssh_low_pass_daily)

    daily_data['filt'] = ssh_filt

    return daily_data
