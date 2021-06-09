                        complt_data = [
                            # normal type eg: HTML
                            {
                                'id1':{
                                    'url':'',
                                    'vid':'',
                                    'like':'',
                                },
                                'id2':{
                                    'url':'',
                                    'vid':'',
                                    'like':'',
                                },
                                'skill':'html',
                                'nested':False
                            },

                            # nested type eg: javascript
                            {
                                'nested': True,
                                'videos': [
                                    {
                                        id: {
                                            'url': '',
                                            'vid': '',
                                            'like': '',
                                        },
                                        id: {
                                            'url': '',
                                            'vid': '',
                                            'like': '',
                                        },
                                        id: {
                                            'url': '',
                                            'vid': '',
                                            'like': '',
                                        },
                                        'skill': 'jquery',
                                    },
                                    {
                                        id: {
                                            'url': '',
                                            'vid': '',
                                            'like': '',
                                        },
                                        'skill': 'angular',
                                    }
                                ],
                                'skill':'javascript'
                            }

                        ]